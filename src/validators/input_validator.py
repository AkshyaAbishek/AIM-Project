"""
Input Validator Module

Validates input data according to business rules and constraints.
"""

import re
import logging
from datetime import datetime, date
from typing import Dict, Any, List, Optional, NamedTuple


class ValidationResult(NamedTuple):
    """Result of input validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    validated_data: Dict[str, Any]


class InputValidator:
    """
    Validates FAST UI input data according to business rules and constraints.
    """
    
    def __init__(self, config_manager):
        """
        Initialize the Input Validator.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
    
    def validate(self, 
                parsed_data: Dict[str, Any], 
                product_type: str,
                validation_level: str = "full") -> ValidationResult:
        """
        Validate parsed input data.
        
        Args:
            parsed_data (dict): Parsed data from FAST UI
            product_type (str): Type of insurance product
            validation_level (str): Level of validation ('basic', 'full', 'strict')
            
        Returns:
            ValidationResult: Result of validation with errors and warnings
        """
        errors = []
        warnings = []
        validated_data = parsed_data.copy()
        
        try:
            validation_rules = self.config_manager.get_validation_rules(product_type)
            
            self.logger.info(f"Starting {validation_level} validation for {product_type}")
            
            # Basic validation (always performed)
            basic_errors, basic_warnings = self._perform_basic_validation(
                validated_data, validation_rules
            )
            errors.extend(basic_errors)
            warnings.extend(basic_warnings)
            
            # Full validation (includes business rules)
            if validation_level in ["full", "strict"]:
                business_errors, business_warnings = self._perform_business_validation(
                    validated_data, validation_rules, product_type
                )
                errors.extend(business_errors)
                warnings.extend(business_warnings)
            
            # Strict validation (includes cross-field validations)
            if validation_level == "strict":
                strict_errors, strict_warnings = self._perform_strict_validation(
                    validated_data, validation_rules, product_type
                )
                errors.extend(strict_errors)
                warnings.extend(strict_warnings)
            
            is_valid = len(errors) == 0
            
            self.logger.info(f"Validation completed: Valid={is_valid}, "
                           f"Errors={len(errors)}, Warnings={len(warnings)}")
            
            return ValidationResult(is_valid, errors, warnings, validated_data)
            
        except Exception as e:
            self.logger.error(f"Validation failed with exception: {str(e)}")
            return ValidationResult(False, [f"Validation error: {str(e)}"], [], {})
    
    def _perform_basic_validation(self, 
                                data: Dict[str, Any], 
                                rules: Dict[str, Any]) -> tuple:
        """
        Perform basic field-level validation.
        
        Args:
            data: Input data to validate
            rules: Validation rules configuration
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        basic_rules = rules.get("basic", {})
        
        # Check required fields
        required_fields = basic_rules.get("required_fields", [])
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == "":
                errors.append(f"Required field '{field}' is missing or empty")
        
        # Check field types
        field_types = basic_rules.get("field_types", {})
        for field, expected_type in field_types.items():
            if field in data and data[field] is not None:
                if not self._check_field_type(data[field], expected_type):
                    errors.append(f"Field '{field}' has invalid type. Expected: {expected_type}")
        
        # Check field ranges
        field_ranges = basic_rules.get("field_ranges", {})
        for field, range_config in field_ranges.items():
            if field in data and data[field] is not None:
                range_errors = self._check_field_range(field, data[field], range_config)
                errors.extend(range_errors)
        
        # Check field formats
        field_formats = basic_rules.get("field_formats", {})
        for field, format_config in field_formats.items():
            if field in data and data[field] is not None:
                format_errors = self._check_field_format(field, data[field], format_config)
                errors.extend(format_errors)
        
        return errors, warnings
    
    def _perform_business_validation(self, 
                                   data: Dict[str, Any], 
                                   rules: Dict[str, Any],
                                   product_type: str) -> tuple:
        """
        Perform business rule validation.
        
        Args:
            data: Input data to validate
            rules: Validation rules configuration
            product_type: Product type for specific business rules
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        business_rules = rules.get("business", {})
        
        # Age-related validations
        age_rules = business_rules.get("age_validations", {})
        if age_rules:
            age_errors, age_warnings = self._validate_age_rules(data, age_rules)
            errors.extend(age_errors)
            warnings.extend(age_warnings)
        
        # Coverage amount validations
        coverage_rules = business_rules.get("coverage_validations", {})
        if coverage_rules:
            coverage_errors = self._validate_coverage_rules(data, coverage_rules)
            errors.extend(coverage_errors)
        
        # Product-specific validations
        product_rules = business_rules.get("product_specific", {}).get(product_type, {})
        if product_rules:
            product_errors = self._validate_product_specific_rules(data, product_rules)
            errors.extend(product_errors)
        
        return errors, warnings
    
    def _perform_strict_validation(self, 
                                 data: Dict[str, Any], 
                                 rules: Dict[str, Any],
                                 product_type: str) -> tuple:
        """
        Perform strict cross-field validation.
        
        Args:
            data: Input data to validate
            rules: Validation rules configuration
            product_type: Product type for specific strict rules
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        strict_rules = rules.get("strict", {})
        
        # Cross-field dependencies
        dependencies = strict_rules.get("field_dependencies", [])
        for dependency in dependencies:
            dependency_errors = self._validate_field_dependency(data, dependency)
            errors.extend(dependency_errors)
        
        # Logical consistency checks
        consistency_rules = strict_rules.get("consistency_checks", [])
        for rule in consistency_rules:
            consistency_errors = self._validate_consistency_rule(data, rule)
            errors.extend(consistency_errors)
        
        return errors, warnings
    
    def _check_field_type(self, value: Any, expected_type: str) -> bool:
        """Check if field value matches expected type."""
        type_mapping = {
            "string": str,
            "integer": int,
            "float": (int, float),
            "boolean": bool,
            "date": (str, date, datetime),
            "number": (int, float)
        }
        
        expected_python_type = type_mapping.get(expected_type.lower())
        if expected_python_type is None:
            return True  # Unknown type, skip validation
        
        return isinstance(value, expected_python_type)
    
    def _check_field_range(self, field_name: str, value: Any, range_config: Dict[str, Any]) -> List[str]:
        """Check if field value is within valid range."""
        errors = []
        
        try:
            if "min" in range_config:
                if float(value) < range_config["min"]:
                    errors.append(f"Field '{field_name}' value {value} is below minimum {range_config['min']}")
            
            if "max" in range_config:
                if float(value) > range_config["max"]:
                    errors.append(f"Field '{field_name}' value {value} is above maximum {range_config['max']}")
            
            if "allowed_values" in range_config:
                if value not in range_config["allowed_values"]:
                    errors.append(f"Field '{field_name}' value '{value}' is not in allowed values: {range_config['allowed_values']}")
                    
        except (ValueError, TypeError):
            errors.append(f"Field '{field_name}' value '{value}' cannot be validated for range")
        
        return errors
    
    def _check_field_format(self, field_name: str, value: Any, format_config: Dict[str, Any]) -> List[str]:
        """Check if field value matches required format."""
        errors = []
        
        if "regex" in format_config:
            pattern = format_config["regex"]
            if not re.match(pattern, str(value)):
                errors.append(f"Field '{field_name}' value '{value}' does not match required format")
        
        if "date_format" in format_config:
            try:
                datetime.strptime(str(value), format_config["date_format"])
            except ValueError:
                errors.append(f"Field '{field_name}' value '{value}' does not match date format {format_config['date_format']}")
        
        return errors
    
    def _validate_age_rules(self, data: Dict[str, Any], age_rules: Dict[str, Any]) -> tuple:
        """Validate age-related business rules."""
        errors = []
        warnings = []
        
        if "birth_date" in data:
            try:
                birth_date = datetime.strptime(str(data["birth_date"]), "%Y-%m-%d").date()
                age = (date.today() - birth_date).days // 365
                
                min_age = age_rules.get("min_age", 0)
                max_age = age_rules.get("max_age", 120)
                
                if age < min_age:
                    errors.append(f"Applicant age {age} is below minimum age {min_age}")
                elif age > max_age:
                    errors.append(f"Applicant age {age} is above maximum age {max_age}")
                
                # Age warnings
                warning_age = age_rules.get("warning_age", 65)
                if age >= warning_age:
                    warnings.append(f"Applicant age {age} requires special review")
                    
            except (ValueError, TypeError):
                errors.append("Invalid birth date format for age calculation")
        
        return errors, warnings
    
    def _validate_coverage_rules(self, data: Dict[str, Any], coverage_rules: Dict[str, Any]) -> List[str]:
        """Validate coverage amount business rules."""
        errors = []
        
        if "coverage_amount" in data:
            try:
                coverage = float(data["coverage_amount"])
                
                min_coverage = coverage_rules.get("min_amount", 0)
                max_coverage = coverage_rules.get("max_amount", float('inf'))
                
                if coverage < min_coverage:
                    errors.append(f"Coverage amount {coverage} is below minimum {min_coverage}")
                elif coverage > max_coverage:
                    errors.append(f"Coverage amount {coverage} is above maximum {max_coverage}")
                
            except (ValueError, TypeError):
                errors.append("Invalid coverage amount format")
        
        return errors
    
    def _validate_product_specific_rules(self, data: Dict[str, Any], product_rules: Dict[str, Any]) -> List[str]:
        """Validate product-specific business rules."""
        errors = []
        
        # This would contain product-specific validation logic
        # For example, life insurance vs. annuity specific rules
        
        return errors
    
    def _validate_field_dependency(self, data: Dict[str, Any], dependency: Dict[str, Any]) -> List[str]:
        """Validate field dependencies."""
        errors = []
        
        source_field = dependency.get("source_field")
        dependent_field = dependency.get("dependent_field")
        condition = dependency.get("condition")
        
        if source_field in data and dependent_field in data:
            source_value = data[source_field]
            dependent_value = data[dependent_field]
            
            # Simple dependency validation logic
            if condition == "required_if_present" and source_value and not dependent_value:
                errors.append(f"Field '{dependent_field}' is required when '{source_field}' is provided")
        
        return errors
    
    def _validate_consistency_rule(self, data: Dict[str, Any], rule: Dict[str, Any]) -> List[str]:
        """Validate logical consistency rules."""
        errors = []
        
        # Example: effective_date should be after birth_date
        if rule.get("type") == "date_order":
            earlier_field = rule.get("earlier_field")
            later_field = rule.get("later_field")
            
            if earlier_field in data and later_field in data:
                try:
                    earlier_date = datetime.strptime(str(data[earlier_field]), "%Y-%m-%d").date()
                    later_date = datetime.strptime(str(data[later_field]), "%Y-%m-%d").date()
                    
                    if earlier_date >= later_date:
                        errors.append(f"Date '{earlier_field}' must be before '{later_field}'")
                        
                except ValueError:
                    errors.append(f"Invalid date format for consistency check: {earlier_field}, {later_field}")
        
        return errors
