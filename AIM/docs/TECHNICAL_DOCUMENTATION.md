# AIM - Actuarial Input Mapper - Technical Documentation

## Overview

AIM (Actuarial Input Mapper) is a comprehensive Python solution designed to automate the mapping of inputs from FAST UI to product-specific actuarial calculation engines. This system eliminates manual input mapping, reduces errors, and standardizes the process across different insurance products.

## Architecture

### Core Components

1. **AIM Processor (`aim_processor.py`)**
   - Main orchestrator that coordinates the entire process
   - Handles error management and logging
   - Provides the main API interface

2. **FAST UI Parser (`parsers/fast_ui_parser.py`)**
   - Parses raw FAST UI data into standardized format
   - Handles nested structures and arrays
   - Normalizes field names and data types

3. **Input Validator (`validators/input_validator.py`)**
   - Validates input data according to business rules
   - Supports multiple validation levels (basic, full, strict)
   - Provides detailed error reporting

4. **Field Mapper (`mappers/field_mapper.py`)**
   - Maps FAST UI fields to actuarial calculation fields
   - Supports complex transformations and data type conversions
   - Handles conditional mapping logic

5. **Configuration Manager (`config/config_manager.py`)**
   - Manages all configuration files
   - Provides default configurations
   - Validates configuration integrity

## Data Flow

```
FAST UI Data → Parser → Validator → Mapper → Transformer → Actuarial Inputs
```

### Detailed Process Flow

1. **Input Reception**: Raw FAST UI data is received as JSON
2. **Parsing**: Data is parsed and normalized
3. **Validation**: Input data is validated against business rules
4. **Field Mapping**: FAST UI fields are mapped to actuarial fields
5. **Transformation**: Data transformations are applied
6. **Output Generation**: Final actuarial input structure is created

## Configuration System

### Field Mappings (`field_mappings.json`)

Defines how FAST UI fields map to actuarial calculation fields:

```json
{
  "life": {
    "applicant_first_name": "insured_first_name",
    "applicant_gender": {
      "target_field": "insured_gender",
      "value_mapping": {
        "M": "Male",
        "F": "Female"
      }
    }
  }
}
```

### Validation Rules (`validation_rules.json`)

Defines validation rules for each product type:

```json
{
  "base": {
    "basic": {
      "required_fields": ["applicant_first_name", "applicant_last_name"],
      "field_types": {
        "applicant_birth_date": "date",
        "policy_face_amount": "number"
      }
    }
  }
}
```

### Transformations (`transformations.json`)

Defines data transformations:

```json
{
  "life": [
    {
      "field": "coverage_amount",
      "type": "currency_conversion",
      "from_currency": "USD",
      "to_currency": "USD"
    }
  ]
}
```

### Output Templates (`output_templates.json`)

Defines the structure of actuarial calculation inputs:

```json
{
  "life": {
    "insured_info": {
      "fields": ["insured_first_name", "insured_last_name"],
      "defaults": {
        "insured_gender": "Unknown"
      }
    }
  }
}
```

## Usage Examples

### Basic Usage

```python
from src import AIMProcessor

# Initialize AIM processor
processor = AIMProcessor()

# Process FAST UI data
result = processor.process_fast_ui_input(
    fast_ui_data=input_data,
    product_type="life",
    validation_level="full"
)

if result["status"] == "success":
    actuarial_inputs = result["actuarial_inputs"]
    # Use actuarial_inputs for calculations
```

### Advanced Configuration

```python
# Use custom configuration path
processor = AIMProcessor(config_path="/path/to/custom/config")

# Validate configuration
validation_result = processor.validate_configuration()

# Get supported products
products = processor.get_supported_products()
```

## Error Handling

The system provides comprehensive error handling:

- **ValidationError**: Raised when input validation fails
- **MappingError**: Raised when field mapping fails
- **ParsingError**: Raised when FAST UI parsing fails

Each error includes detailed information about what went wrong and how to fix it.

## Validation Levels

### Basic Validation
- Required field checks
- Data type validation
- Basic range validation

### Full Validation
- All basic validations
- Business rule validation
- Age and coverage amount checks

### Strict Validation
- All full validations
- Cross-field dependency checks
- Logical consistency validation

## Extending the System

### Adding New Products

1. Add field mappings in `field_mappings.json`
2. Add validation rules in `validation_rules.json`
3. Add transformations in `transformations.json`
4. Add output template in `output_templates.json`

### Custom Transformations

Create custom transformation functions in the `AIMProcessor` class:

```python
def _custom_transformation(self, value, config):
    # Custom transformation logic
    return transformed_value
```

### Custom Validators

Extend the `InputValidator` class with custom validation methods:

```python
def _validate_custom_rule(self, data, rule):
    # Custom validation logic
    return errors
```

## Performance Considerations

- **Configuration Caching**: Configurations are loaded once and cached
- **Lazy Loading**: Only necessary modules are loaded
- **Memory Management**: Large datasets are processed in chunks
- **Logging**: Comprehensive logging for performance monitoring

## Security Considerations

- **Input Sanitization**: All inputs are sanitized before processing
- **Configuration Validation**: All configurations are validated on startup
- **Error Handling**: Sensitive information is not exposed in error messages
- **Audit Trail**: Complete audit trail of all transformations

## Testing

### Unit Tests
Run unit tests for individual components:
```bash
pytest tests/unit/
```

### Integration Tests
Run integration tests for end-to-end functionality:
```bash
pytest tests/integration/
```

### Configuration Tests
Validate all configuration files:
```python
processor = AIMProcessor()
result = processor.validate_configuration()
```

## Monitoring and Logging

The system provides comprehensive logging:

- **Info Level**: Normal processing information
- **Warning Level**: Potential issues that don't stop processing
- **Error Level**: Errors that stop processing
- **Debug Level**: Detailed debugging information

Log files are created automatically in the working directory.

## Deployment

### Production Deployment

1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment-specific settings
3. Validate configuration: Run configuration validation
4. Set up monitoring and alerting
5. Deploy to production environment

### Configuration Management

- Use environment-specific configuration files
- Implement configuration versioning
- Monitor configuration changes
- Validate configurations before deployment

## Troubleshooting

### Common Issues

1. **Missing Required Fields**: Check validation rules and input data
2. **Mapping Errors**: Verify field mapping configuration
3. **Validation Failures**: Review business rules and input values
4. **Configuration Errors**: Validate configuration files

### Debug Mode

Enable debug logging to get detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Support and Maintenance

- **Regular Updates**: Keep dependencies updated
- **Configuration Reviews**: Regularly review and update configurations
- **Performance Monitoring**: Monitor processing times and error rates
- **Documentation**: Keep documentation updated with changes
