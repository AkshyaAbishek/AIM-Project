"""
Actuarial Input Builder - Example Usage

This script demonstrates how to use the Actuarial Input Builder to process
FAST UI inputs and convert them to actuarial calculation format.
"""

import json
import sys
import os
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from input_builder import ActurialInputBuilder, ValidationError, MappingError


def run_example():
    """Run example processing of FAST UI data."""
    
    print("🏗️  Actuarial Input Builder - Example Usage")
    print("=" * 50)
    
    # Initialize the input builder
    print("\n1. Initializing Actuarial Input Builder...")
    try:
        builder = ActurialInputBuilder()
        print("✅ Input Builder initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Input Builder: {e}")
        return
    
    # Show supported products
    print("\n2. Checking supported products...")
    supported_products = builder.get_supported_products()
    print(f"✅ Supported products: {', '.join(supported_products)}")
    
    # Load sample FAST UI data
    print("\n3. Loading sample FAST UI data...")
    try:
        sample_file = os.path.join("data", "sample", "life_insurance_sample.json")
        with open(sample_file, 'r') as f:
            fast_ui_data = json.load(f)
        print(f"✅ Loaded sample data with {len(fast_ui_data)} top-level fields")
        print(f"   Sample fields: {list(fast_ui_data.keys())[:5]}...")
    except FileNotFoundError:
        print("❌ Sample data file not found, using minimal example")
        fast_ui_data = {
            "applicant_first_name": "John",
            "applicant_last_name": "Doe",
            "applicant_birth_date": "1985-06-15",
            "applicant_gender": "M",
            "policy_face_amount": "250000",
            "policy_effective_date": "2024-01-01",
            "premium_mode": "M"
        }
    
    # Process the data for different product types
    product_types = ["life", "annuity", "health"]
    
    for product_type in product_types:
        print(f"\n4. Processing data for product type: {product_type}")
        print("-" * 40)
        
        try:
            # Process with full validation
            result = builder.process_fast_ui_input(
                fast_ui_data=fast_ui_data,
                product_type=product_type,
                validation_level="full"
            )
            
            if result["status"] == "success":
                print(f"✅ Processing successful for {product_type}")
                print(f"   ⏱️  Processing time: {result['processing_time']:.2f}s")
                print(f"   📊 Fields processed: {result['metadata']['fields_processed']}")
                print(f"   🎯 Fields mapped: {result['metadata']['fields_mapped']}")
                
                # Show sample of actuarial inputs
                actuarial_inputs = result["actuarial_inputs"]
                print(f"   📋 Actuarial input sections: {list(actuarial_inputs.keys())}")
                
                # Show first section details
                if actuarial_inputs:
                    first_section = list(actuarial_inputs.keys())[0]
                    first_section_data = actuarial_inputs[first_section]
                    print(f"   📝 Sample section '{first_section}': {first_section_data}")
            
            else:
                print(f"❌ Processing failed for {product_type}")
                print(f"   Error: {result.get('error_message', 'Unknown error')}")
        
        except Exception as e:
            print(f"❌ Exception during processing: {e}")
    
    # Demonstrate validation configuration
    print(f"\n5. Validating configuration...")
    config_validation = builder.validate_configuration()
    
    if config_validation["is_valid"]:
        print("✅ Configuration is valid")
    else:
        print("⚠️  Configuration has issues:")
        for error in config_validation["errors"]:
            print(f"   ❌ {error}")
    
    if config_validation["warnings"]:
        print("   Warnings:")
        for warning in config_validation["warnings"]:
            print(f"   ⚠️  {warning}")
    
    # Show product coverage
    print("\n6. Product Configuration Coverage:")
    for product, coverage in config_validation["product_coverage"].items():
        print(f"   📦 {product}:")
        for config_type, has_config in coverage.items():
            status = "✅" if has_config else "❌"
            print(f"      {status} {config_type.replace('_', ' ').title()}")


def run_interactive_demo():
    """Run an interactive demo where user can input their own data."""
    
    print("\n" + "=" * 50)
    print("🎮 Interactive Demo Mode")
    print("=" * 50)
    
    builder = ActurialInputBuilder()
    
    while True:
        print("\nOptions:")
        print("1. Process sample life insurance data")
        print("2. Enter custom JSON data")
        print("3. Show field mapping for a product")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            # Use sample data
            sample_data = {
                "applicant_first_name": "Alice",
                "applicant_last_name": "Johnson",
                "applicant_birth_date": "1990-03-20",
                "applicant_gender": "F",
                "policy_face_amount": "500000",
                "policy_effective_date": "2024-02-01",
                "premium_mode": "Q"
            }
            
            print("\n📄 Processing sample data:")
            print(json.dumps(sample_data, indent=2))
            
            result = builder.process_fast_ui_input(sample_data, "life", "full")
            print_result(result)
        
        elif choice == "2":
            # Custom JSON input
            print("\n📝 Enter your JSON data (or 'cancel' to go back):")
            print("Example: {\"applicant_first_name\": \"John\", \"applicant_last_name\": \"Doe\"}")
            
            json_input = input("\nJSON: ").strip()
            
            if json_input.lower() == 'cancel':
                continue
            
            try:
                custom_data = json.loads(json_input)
                product_type = input("Enter product type (life/annuity/health): ").strip().lower()
                
                if product_type in ["life", "annuity", "health"]:
                    result = builder.process_fast_ui_input(custom_data, product_type, "full")
                    print_result(result)
                else:
                    print("❌ Invalid product type")
            
            except json.JSONDecodeError:
                print("❌ Invalid JSON format")
        
        elif choice == "3":
            # Show field mappings
            product_type = input("Enter product type (life/annuity/health): ").strip().lower()
            
            if product_type in ["life", "annuity", "health"]:
                mappings = builder.mapper.get_mapping_summary(product_type)
                print(f"\n📋 Field mappings for {product_type}:")
                print(f"   Total mappings: {mappings['total_mappings']}")
                print(f"   Simple mappings: {mappings['simple_mappings']}")
                print(f"   Complex mappings: {mappings['complex_mappings']}")
                
                print("\n   Field details:")
                for field_info in mappings['field_list'][:5]:  # Show first 5
                    print(f"   • {field_info['fast_ui_field']} → {field_info['target_field']} ({field_info['type']})")
                
                if len(mappings['field_list']) > 5:
                    print(f"   ... and {len(mappings['field_list']) - 5} more fields")
            else:
                print("❌ Invalid product type")
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")


def print_result(result):
    """Print processing result in a formatted way."""
    if result["status"] == "success":
        print(f"\n✅ Processing successful!")
        print(f"   ⏱️  Time: {result['processing_time']:.2f}s")
        print(f"   📊 Fields: {result['metadata']['fields_processed']} → {result['metadata']['fields_mapped']}")
        
        print(f"\n📋 Actuarial inputs:")
        for section_name, section_data in result["actuarial_inputs"].items():
            print(f"   📦 {section_name}:")
            for field_name, field_value in section_data.items():
                print(f"      • {field_name}: {field_value}")
    else:
        print(f"\n❌ Processing failed:")
        print(f"   Error: {result.get('error_message', 'Unknown error')}")


if __name__ == "__main__":
    print("🚀 Starting Actuarial Input Builder Examples")
    
    try:
        # Run basic example
        run_example()
        
        # Ask if user wants to try interactive demo
        response = input("\n🎮 Would you like to try the interactive demo? (y/n): ").strip().lower()
        
        if response in ['y', 'yes']:
            run_interactive_demo()
        
    except KeyboardInterrupt:
        print("\n\n👋 Example terminated by user")
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🏁 Example completed")
