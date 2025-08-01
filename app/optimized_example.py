"""
AIM - Actuarial Input Mapper - Optimized Example

This module demonstrates the optimized usage of AIM processor with proper error handling,
code organization, and best practices.
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Union, Any, Optional

# Add src directory to path for imports
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from aim_processor import AIMProcessor, ValidationError, MappingError


class OptimizedExample:
    """
    Demonstrates optimized usage of AIM processor with proper error handling
    and organized code structure.
    """
    
    def __init__(self):
        """Initialize the example with AIM processor."""
        self.processor = AIMProcessor()
        self.results_store = []
    
    def initialize_processor(self) -> bool:
        """Initialize processor with proper error handling."""
        try:
            print("✅ AIM Processor initialized successfully")
            return True
        except Exception as error:
            print(f"❌ Failed to initialize AIM Processor: {error}")
            return False
    
    def process_sample_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a sample input file with proper error handling.
        
        Args:
            file_path: Path to the input file (JSON or Excel)
            
        Returns:
            Dict containing processing results
        """
        try:
            # Load and validate input file
            if file_path.lower().endswith(('.xlsx', '.xls')):
                import pandas as pd
                df = pd.read_excel(file_path)
                data = df.to_dict(orient='records')
                data = {"records": data, "source": "excel"}
            else:
                with open(file_path, 'r') as f:
                    data = json.load(f)
            
            print(f"✅ Loaded input file with {len(data)} fields")
            
            # Process through AIM processor
            result = self.processor.process_data(data)
            
            if result:
                print("✅ Processing completed successfully")
                print(f"⏱️  Completed at: {datetime.now().isoformat()}")
                
                for key, value in result.items():
                    print(f"📊 {key}: {value}")
                    
                self.results_store.append(result)
                return result
            else:
                print("❌ Processing failed")
                return {"status": "failed"}
                
        except ValidationError as validation_error:
            print(f"❌ Validation error: {validation_error}")
            return {"status": "error", "error": str(validation_error)}
        except Exception as error:
            print(f"❌ Unexpected error: {error}")
            return {"status": "error", "error": str(error)}
    
    def run_example(self) -> None:
        """Run the optimized example with proper error handling."""
        print("\n🚀 Starting AIM Optimized Example")
        print("=" * 50)
        
        if not self.initialize_processor():
            return
        
        # Process sample life insurance data
        print("\n1. Processing Life Insurance Sample")
        print("-" * 40)
        
        sample_file = os.path.join(project_root, "data", "sample", "life_insurance_sample.json")
        result = self.process_sample_file(sample_file)
        
        # Show processing summary
        print("\n📋 Processing Summary")
        print("=" * 50)
        
        successful = sum(1 for r in self.results_store if r.get("status") != "failed")
        print(f"📊 Total processed: {len(self.results_store)}")
        print(f"✅ Successful: {successful}")
        print(f"📈 Success rate: {(successful/len(self.results_store))*100 if self.results_store else 0}%")


def main():
    """Main entry point with proper error handling."""
    try:
        example = OptimizedExample()
        example.run_example()
    except KeyboardInterrupt:
        print("\n⚠️  Example terminated by user")
    except Exception as error:
        print(f"❌ Example failed with error: {error}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
