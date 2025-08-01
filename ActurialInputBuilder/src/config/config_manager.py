"""
Configuration Manager Module

Manages configuration files and settings for the Actuarial Input Builder.
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional


class ConfigManager:
    """
    Manages configuration for field mappings, validation rules, and transformations.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Configuration Manager.
        
        Args:
            config_path (str, optional): Path to custom configuration directory
        """
        self.logger = logging.getLogger(__name__)
        
        # Set default config path if not provided
        if config_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, "config_files")
        
        self.config_path = config_path
        self._ensure_config_directory()
        
        # Load configurations
        self.field_mappings = self._load_field_mappings()
        self.validation_rules = self._load_validation_rules()
        self.transformations = self._load_transformations()
        self.output_templates = self._load_output_templates()
        
        self.logger.info(f"Configuration Manager initialized with path: {config_path}")
    
    def _ensure_config_directory(self):
        """Ensure configuration directory exists and create default files if needed."""
        os.makedirs(self.config_path, exist_ok=True)
        
        # Create default configuration files if they don't exist
        default_configs = {
            "field_mappings.json": self._get_default_field_mappings(),
            "validation_rules.json": self._get_default_validation_rules(),
            "transformations.json": self._get_default_transformations(),
            "output_templates.json": self._get_default_output_templates()
        }
        
        for filename, default_content in default_configs.items():
            file_path = os.path.join(self.config_path, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(default_content, f, indent=2)
                self.logger.info(f"Created default configuration file: {filename}")
    
    def _load_field_mappings(self) -> Dict[str, Any]:
        """Load field mapping configurations."""
        return self._load_json_config("field_mappings.json")
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rule configurations."""
        return self._load_json_config("validation_rules.json")
    
    def _load_transformations(self) -> Dict[str, Any]:
        """Load transformation configurations."""
        return self._load_json_config("transformations.json")
    
    def _load_output_templates(self) -> Dict[str, Any]:
        """Load output template configurations."""
        return self._load_json_config("output_templates.json")
    
    def _load_json_config(self, filename: str) -> Dict[str, Any]:
        """
        Load a JSON configuration file.
        
        Args:
            filename: Name of the configuration file
            
        Returns:
            Configuration data as dictionary
        """
        file_path = os.path.join(self.config_path, filename)
        
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
            self.logger.info(f"Loaded configuration: {filename}")
            return config
        except FileNotFoundError:
            self.logger.warning(f"Configuration file not found: {filename}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file {filename}: {str(e)}")
            return {}
    
    def get_field_mappings(self, product_type: str) -> Dict[str, Any]:
        """
        Get field mappings for a specific product type.
        
        Args:
            product_type: Product type (e.g., 'life', 'annuity', 'health')
            
        Returns:
            Field mappings for the product type
        """
        return self.field_mappings.get(product_type, {})
    
    def get_validation_rules(self, product_type: str) -> Dict[str, Any]:
        """
        Get validation rules for a specific product type.
        
        Args:
            product_type: Product type
            
        Returns:
            Validation rules for the product type
        """
        # Get base rules and merge with product-specific rules
        base_rules = self.validation_rules.get("base", {})
        product_rules = self.validation_rules.get(product_type, {})
        
        # Deep merge the rules
        merged_rules = self._deep_merge(base_rules, product_rules)
        return merged_rules
    
    def get_transformations(self, product_type: str) -> List[Dict[str, Any]]:
        """
        Get transformations for a specific product type.
        
        Args:
            product_type: Product type
            
        Returns:
            List of transformation configurations
        """
        return self.transformations.get(product_type, [])
    
    def get_output_template(self, product_type: str) -> Dict[str, Any]:
        """
        Get output template for a specific product type.
        
        Args:
            product_type: Product type
            
        Returns:
            Output template configuration
        """
        return self.output_templates.get(product_type, {})
    
    def get_supported_products(self) -> List[str]:
        """
        Get list of supported product types.
        
        Returns:
            List of supported product types
        """
        # Get unique product types from all configurations
        products = set()
        
        products.update(self.field_mappings.keys())
        products.update(self.validation_rules.keys())
        products.update(self.transformations.keys())
        products.update(self.output_templates.keys())
        
        # Remove 'base' as it's not a product type
        products.discard('base')
        
        return sorted(list(products))
    
    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate the current configuration setup.
        
        Returns:
            Validation results
        """
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "product_coverage": {}
        }
        
        supported_products = self.get_supported_products()
        
        for product in supported_products:
            product_validation = {
                "has_field_mappings": bool(self.get_field_mappings(product)),
                "has_validation_rules": bool(self.get_validation_rules(product)),
                "has_transformations": bool(self.get_transformations(product)),
                "has_output_template": bool(self.get_output_template(product))
            }
            
            validation_results["product_coverage"][product] = product_validation
            
            # Check for missing configurations
            if not product_validation["has_field_mappings"]:
                validation_results["warnings"].append(f"No field mappings defined for product: {product}")
            
            if not product_validation["has_validation_rules"]:
                validation_results["warnings"].append(f"No validation rules defined for product: {product}")
        
        # Check if any warnings should be treated as errors
        if len(validation_results["warnings"]) > len(supported_products):
            validation_results["is_valid"] = False
            validation_results["errors"].append("Too many missing configurations")
        
        return validation_results
    
    def _deep_merge(self, base_dict: Dict[str, Any], overlay_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries.
        
        Args:
            base_dict: Base dictionary
            overlay_dict: Dictionary to overlay on base
            
        Returns:
            Merged dictionary
        """
        result = base_dict.copy()
        
        for key, value in overlay_dict.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _get_default_field_mappings(self) -> Dict[str, Any]:
        """Get default field mapping configuration."""
        return {
            "life": {
                "applicant_first_name": "insured_first_name",
                "applicant_last_name": "insured_last_name",
                "applicant_birth_date": "insured_birth_date",
                "applicant_gender": {
                    "target_field": "insured_gender",
                    "value_mapping": {
                        "M": "Male",
                        "F": "Female",
                        "Male": "Male",
                        "Female": "Female"
                    }
                },
                "policy_face_amount": {
                    "target_field": "coverage_amount",
                    "data_type": "float"
                },
                "policy_effective_date": "policy_start_date",
                "premium_mode": {
                    "target_field": "premium_frequency",
                    "value_mapping": {
                        "A": "Annual",
                        "SA": "Semi-Annual",
                        "Q": "Quarterly",
                        "M": "Monthly"
                    }
                }
            },
            "annuity": {
                "annuitant_first_name": "annuitant_first_name",
                "annuitant_last_name": "annuitant_last_name",
                "annuitant_birth_date": "annuitant_birth_date",
                "initial_premium": {
                    "target_field": "premium_amount",
                    "data_type": "float"
                },
                "annuity_start_date": "contract_start_date"
            },
            "health": {
                "member_first_name": "member_first_name",
                "member_last_name": "member_last_name",
                "member_birth_date": "member_birth_date",
                "plan_type": "coverage_type",
                "deductible_amount": {
                    "target_field": "deductible",
                    "data_type": "float"
                }
            }
        }
    
    def _get_default_validation_rules(self) -> Dict[str, Any]:
        """Get default validation rule configuration."""
        return {
            "base": {
                "basic": {
                    "required_fields": ["applicant_first_name", "applicant_last_name", "applicant_birth_date"],
                    "field_types": {
                        "applicant_first_name": "string",
                        "applicant_last_name": "string",
                        "applicant_birth_date": "date",
                        "policy_face_amount": "number",
                        "premium_amount": "number"
                    },
                    "field_ranges": {
                        "policy_face_amount": {"min": 1000, "max": 10000000},
                        "premium_amount": {"min": 10, "max": 100000}
                    },
                    "field_formats": {
                        "applicant_birth_date": {"date_format": "%Y-%m-%d"}
                    }
                },
                "business": {
                    "age_validations": {
                        "min_age": 18,
                        "max_age": 85,
                        "warning_age": 65
                    },
                    "coverage_validations": {
                        "min_amount": 1000,
                        "max_amount": 5000000
                    }
                },
                "strict": {
                    "field_dependencies": [
                        {
                            "source_field": "beneficiary_name",
                            "dependent_field": "beneficiary_relationship",
                            "condition": "required_if_present"
                        }
                    ],
                    "consistency_checks": [
                        {
                            "type": "date_order",
                            "earlier_field": "applicant_birth_date",
                            "later_field": "policy_effective_date"
                        }
                    ]
                }
            },
            "life": {
                "business": {
                    "age_validations": {
                        "min_age": 18,
                        "max_age": 80
                    },
                    "coverage_validations": {
                        "min_amount": 10000,
                        "max_amount": 10000000
                    }
                }
            },
            "annuity": {
                "business": {
                    "age_validations": {
                        "min_age": 18,
                        "max_age": 85
                    }
                }
            }
        }
    
    def _get_default_transformations(self) -> Dict[str, Any]:
        """Get default transformation configuration."""
        return {
            "life": [
                {
                    "field": "coverage_amount",
                    "type": "currency_conversion",
                    "from_currency": "USD",
                    "to_currency": "USD"
                }
            ],
            "annuity": [
                {
                    "field": "premium_amount",
                    "type": "currency_conversion",
                    "from_currency": "USD",
                    "to_currency": "USD"
                }
            ]
        }
    
    def _get_default_output_templates(self) -> Dict[str, Any]:
        """Get default output template configuration."""
        return {
            "life": {
                "insured_info": {
                    "fields": ["insured_first_name", "insured_last_name", "insured_birth_date", "insured_gender"],
                    "defaults": {
                        "insured_gender": "Unknown"
                    }
                },
                "policy_info": {
                    "fields": ["coverage_amount", "policy_start_date", "premium_frequency"],
                    "defaults": {
                        "premium_frequency": "Monthly"
                    }
                },
                "calculation_inputs": {
                    "fields": ["coverage_amount", "insured_birth_date", "premium_frequency"],
                    "defaults": {}
                }
            },
            "annuity": {
                "annuitant_info": {
                    "fields": ["annuitant_first_name", "annuitant_last_name", "annuitant_birth_date"],
                    "defaults": {}
                },
                "contract_info": {
                    "fields": ["premium_amount", "contract_start_date"],
                    "defaults": {}
                }
            },
            "health": {
                "member_info": {
                    "fields": ["member_first_name", "member_last_name", "member_birth_date"],
                    "defaults": {}
                },
                "coverage_info": {
                    "fields": ["coverage_type", "deductible"],
                    "defaults": {
                        "deductible": 0
                    }
                }
            }
        }
