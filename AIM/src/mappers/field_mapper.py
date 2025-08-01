"""
Field Mapper Module

Handles the mapping of fields from FAST UI format to actuarial calculation format.
"""

import json
import logging
from typing import Dict, Any, List, Optional


class FieldMapper:
    """
    Maps fields from FAST UI format to product-specific actuarial calculation format.
    """
    
    def __init__(self, config_manager):
        """
        Initialize the Field Mapper.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
    
    def map_fields(self, parsed_data: Dict[str, Any], product_type: str) -> Dict[str, Any]:
        """
        Map FAST UI fields to actuarial calculation fields.
        
        Args:
            parsed_data (dict): Parsed data from FAST UI
            product_type (str): Type of insurance product
            
        Returns:
            dict: Mapped data for actuarial calculations
            
        Raises:
            MappingError: If field mapping fails
        """
        try:
            mapping_config = self.config_manager.get_field_mappings(product_type)
            mapped_data = {}
            
            for fast_ui_field, actuarial_field_config in mapping_config.items():
                if fast_ui_field in parsed_data:
                    mapped_value = self._map_field_value(
                        parsed_data[fast_ui_field],
                        actuarial_field_config
                    )
                    
                    # Handle nested field mapping
                    if isinstance(actuarial_field_config, dict) and "target_field" in actuarial_field_config:
                        target_field = actuarial_field_config["target_field"]
                        mapped_data[target_field] = mapped_value
                    elif isinstance(actuarial_field_config, str):
                        mapped_data[actuarial_field_config] = mapped_value
                    else:
                        self.logger.warning(f"Invalid mapping configuration for field: {fast_ui_field}")
            
            self.logger.info(f"Successfully mapped {len(mapped_data)} fields for product type: {product_type}")
            return mapped_data
            
        except Exception as e:
            self.logger.error(f"Field mapping failed: {str(e)}")
            raise MappingError(f"Failed to map fields: {str(e)}")
    
    def _map_field_value(self, value: Any, field_config: Any) -> Any:
        """
        Map a single field value according to its configuration.
        
        Args:
            value: Original value from FAST UI
            field_config: Configuration for mapping this field
            
        Returns:
            Mapped value for actuarial calculation
        """
        if isinstance(field_config, str):
            # Simple direct mapping
            return value
        
        if isinstance(field_config, dict):
            # Complex mapping with transformations
            mapped_value = value
            
            # Apply data type conversion
            if "data_type" in field_config:
                mapped_value = self._convert_data_type(mapped_value, field_config["data_type"])
            
            # Apply value mapping (e.g., enum mappings)
            if "value_mapping" in field_config:
                mapped_value = self._apply_value_mapping(mapped_value, field_config["value_mapping"])
            
            # Apply scaling or mathematical transformations
            if "scale_factor" in field_config:
                if isinstance(mapped_value, (int, float)):
                    mapped_value = mapped_value * field_config["scale_factor"]
            
            # Apply conditional logic
            if "conditions" in field_config:
                mapped_value = self._apply_conditions(mapped_value, field_config["conditions"])
            
            return mapped_value
        
        return value
    
    def _convert_data_type(self, value: Any, target_type: str) -> Any:
        """
        Convert value to target data type.
        
        Args:
            value: Original value
            target_type: Target data type ('int', 'float', 'str', 'bool')
            
        Returns:
            Converted value
        """
        try:
            if target_type == "int":
                return int(float(str(value)))
            elif target_type == "float":
                return float(str(value))
            elif target_type == "str":
                return str(value)
            elif target_type == "bool":
                if isinstance(value, str):
                    return value.lower() in ("true", "yes", "1", "on")
                return bool(value)
            else:
                self.logger.warning(f"Unknown data type: {target_type}")
                return value
        except (ValueError, TypeError) as e:
            self.logger.warning(f"Data type conversion failed: {e}")
            return value
    
    def _apply_value_mapping(self, value: Any, value_mapping: Dict[str, Any]) -> Any:
        """
        Apply value mapping transformations.
        
        Args:
            value: Original value
            value_mapping: Dictionary mapping original values to new values
            
        Returns:
            Mapped value
        """
        str_value = str(value)
        return value_mapping.get(str_value, value)
    
    def _apply_conditions(self, value: Any, conditions: List[Dict[str, Any]]) -> Any:
        """
        Apply conditional transformations.
        
        Args:
            value: Original value
            conditions: List of condition dictionaries
            
        Returns:
            Transformed value based on conditions
        """
        for condition in conditions:
            if self._evaluate_condition(value, condition):
                return condition.get("result", value)
        
        return value
    
    def _evaluate_condition(self, value: Any, condition: Dict[str, Any]) -> bool:
        """
        Evaluate a single condition.
        
        Args:
            value: Value to evaluate
            condition: Condition configuration
            
        Returns:
            True if condition is met, False otherwise
        """
        operator = condition.get("operator", "eq")
        compare_value = condition.get("value")
        
        try:
            if operator == "eq":
                return value == compare_value
            elif operator == "ne":
                return value != compare_value
            elif operator == "gt":
                return float(value) > float(compare_value)
            elif operator == "gte":
                return float(value) >= float(compare_value)
            elif operator == "lt":
                return float(value) < float(compare_value)
            elif operator == "lte":
                return float(value) <= float(compare_value)
            elif operator == "in":
                return value in compare_value
            elif operator == "not_in":
                return value not in compare_value
            else:
                self.logger.warning(f"Unknown operator: {operator}")
                return False
        except (ValueError, TypeError):
            return False
    
    def get_mapping_summary(self, product_type: str) -> Dict[str, Any]:
        """
        Get a summary of field mappings for a product type.
        
        Args:
            product_type: Product type to summarize
            
        Returns:
            Summary of field mappings
        """
        mapping_config = self.config_manager.get_field_mappings(product_type)
        
        summary = {
            "product_type": product_type,
            "total_mappings": len(mapping_config),
            "simple_mappings": 0,
            "complex_mappings": 0,
            "field_list": []
        }
        
        for fast_ui_field, actuarial_config in mapping_config.items():
            field_info = {"fast_ui_field": fast_ui_field}
            
            if isinstance(actuarial_config, str):
                summary["simple_mappings"] += 1
                field_info["type"] = "simple"
                field_info["target_field"] = actuarial_config
            else:
                summary["complex_mappings"] += 1
                field_info["type"] = "complex"
                field_info["target_field"] = actuarial_config.get("target_field", "unknown")
                field_info["transformations"] = list(actuarial_config.keys())
            
            summary["field_list"].append(field_info)
        
        return summary


class MappingError(Exception):
    """Exception raised when field mapping fails."""
    pass
