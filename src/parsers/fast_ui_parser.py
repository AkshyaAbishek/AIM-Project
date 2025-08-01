"""
FAST UI Parser Module

Parses input data from FAST UI format into a standardized format.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime


class FastUIParser:
    """
    Parses input data from FAST UI format into a standardized internal format.
    """
    
    def __init__(self):
        """Initialize the FAST UI Parser."""
        self.logger = logging.getLogger(__name__)
    
    def parse(self, fast_ui_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse FAST UI data into standardized format.
        
        Args:
            fast_ui_data (dict): Raw input data from FAST UI
            
        Returns:
            dict: Parsed data in standardized format
            
        Raises:
            ParsingError: If parsing fails
        """
        try:
            self.logger.info("Starting FAST UI data parsing")
            
            parsed_data = {}
            
            # Handle different FAST UI data structures
            if self._is_nested_structure(fast_ui_data):
                parsed_data = self._parse_nested_structure(fast_ui_data)
            else:
                parsed_data = self._parse_flat_structure(fast_ui_data)
            
            # Clean and normalize data
            cleaned_data = self._clean_data(parsed_data)
            
            # Add parsing metadata
            cleaned_data["_parsing_metadata"] = {
                "parsed_at": datetime.now().isoformat(),
                "original_fields_count": len(fast_ui_data),
                "parsed_fields_count": len(cleaned_data) - 1,  # Exclude metadata
                "parser_version": "1.0.0"
            }
            
            self.logger.info(f"Successfully parsed {len(cleaned_data)} fields")
            return cleaned_data
            
        except Exception as e:
            self.logger.error(f"FAST UI parsing failed: {str(e)}")
            raise ParsingError(f"Failed to parse FAST UI data: {str(e)}")
    
    def _is_nested_structure(self, data: Dict[str, Any]) -> bool:
        """
        Check if the FAST UI data has nested structure.
        
        Args:
            data: FAST UI data to check
            
        Returns:
            True if data has nested structure, False otherwise
        """
        # Check for common nested structure indicators
        nested_indicators = ["applicant", "policy", "coverage", "beneficiary", "sections"]
        
        for indicator in nested_indicators:
            if indicator in data and isinstance(data[indicator], dict):
                return True
        
        # Check if any values are dictionaries (indicating nesting)
        for value in data.values():
            if isinstance(value, dict):
                return True
        
        return False
    
    def _parse_nested_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse nested FAST UI data structure.
        
        Args:
            data: Nested FAST UI data
            
        Returns:
            Flattened parsed data
        """
        parsed_data = {}
        
        for section_name, section_data in data.items():
            if isinstance(section_data, dict):
                # Flatten nested sections with prefixes
                for field_name, field_value in section_data.items():
                    flattened_key = f"{section_name}_{field_name}"
                    parsed_data[flattened_key] = self._parse_field_value(field_value)
            elif isinstance(section_data, list):
                # Handle arrays (e.g., multiple beneficiaries)
                parsed_data.update(self._parse_array_section(section_name, section_data))
            else:
                # Simple field
                parsed_data[section_name] = self._parse_field_value(section_data)
        
        return parsed_data
    
    def _parse_flat_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse flat FAST UI data structure.
        
        Args:
            data: Flat FAST UI data
            
        Returns:
            Parsed data
        """
        parsed_data = {}
        
        for field_name, field_value in data.items():
            parsed_data[field_name] = self._parse_field_value(field_value)
        
        return parsed_data
    
    def _parse_array_section(self, section_name: str, array_data: List[Any]) -> Dict[str, Any]:
        """
        Parse array sections (like multiple beneficiaries).
        
        Args:
            section_name: Name of the section
            array_data: Array of data items
            
        Returns:
            Flattened data with indexed keys
        """
        parsed_data = {}
        
        for index, item in enumerate(array_data):
            if isinstance(item, dict):
                for field_name, field_value in item.items():
                    indexed_key = f"{section_name}_{index + 1}_{field_name}"
                    parsed_data[indexed_key] = self._parse_field_value(field_value)
            else:
                indexed_key = f"{section_name}_{index + 1}"
                parsed_data[indexed_key] = self._parse_field_value(item)
        
        # Also store the count
        parsed_data[f"{section_name}_count"] = len(array_data)
        
        return parsed_data
    
    def _parse_field_value(self, value: Any) -> Any:
        """
        Parse and clean individual field values.
        
        Args:
            value: Raw field value
            
        Returns:
            Cleaned and parsed field value
        """
        if value is None:
            return None
        
        # Handle string values
        if isinstance(value, str):
            # Remove extra whitespace
            cleaned_value = value.strip()
            
            # Try to parse as number if it looks like one
            if self._looks_like_number(cleaned_value):
                return self._parse_number(cleaned_value)
            
            # Try to parse as boolean
            if self._looks_like_boolean(cleaned_value):
                return self._parse_boolean(cleaned_value)
            
            # Try to parse as date
            if self._looks_like_date(cleaned_value):
                return self._parse_date(cleaned_value)
            
            return cleaned_value
        
        # Handle numeric values
        elif isinstance(value, (int, float)):
            return value
        
        # Handle boolean values
        elif isinstance(value, bool):
            return value
        
        # Handle nested objects recursively
        elif isinstance(value, dict):
            return {k: self._parse_field_value(v) for k, v in value.items()}
        
        # Handle arrays
        elif isinstance(value, list):
            return [self._parse_field_value(item) for item in value]
        
        # Return as-is for other types
        else:
            return value
    
    def _looks_like_number(self, value: str) -> bool:
        """Check if string looks like a number."""
        # Remove common number formatting
        cleaned = value.replace(",", "").replace("$", "").strip()
        
        try:
            float(cleaned)
            return True
        except ValueError:
            return False
    
    def _parse_number(self, value: str) -> float:
        """Parse string as number."""
        # Remove common formatting
        cleaned = value.replace(",", "").replace("$", "").strip()
        
        try:
            # Try integer first
            if "." not in cleaned:
                return int(cleaned)
            else:
                return float(cleaned)
        except ValueError:
            return value  # Return original if parsing fails
    
    def _looks_like_boolean(self, value: str) -> bool:
        """Check if string looks like a boolean."""
        boolean_values = {"true", "false", "yes", "no", "y", "n", "1", "0", "on", "off"}
        return value.lower() in boolean_values
    
    def _parse_boolean(self, value: str) -> bool:
        """Parse string as boolean."""
        true_values = {"true", "yes", "y", "1", "on"}
        return value.lower() in true_values
    
    def _looks_like_date(self, value: str) -> bool:
        """Check if string looks like a date."""
        date_patterns = [
            r"^\d{4}-\d{2}-\d{2}$",  # YYYY-MM-DD
            r"^\d{2}/\d{2}/\d{4}$",  # MM/DD/YYYY
            r"^\d{2}-\d{2}-\d{4}$",  # MM-DD-YYYY
            r"^\d{1,2}/\d{1,2}/\d{4}$",  # M/D/YYYY
        ]
        
        import re
        for pattern in date_patterns:
            if re.match(pattern, value):
                return True
        
        return False
    
    def _parse_date(self, value: str) -> str:
        """Parse and normalize date string."""
        import re
        from datetime import datetime
        
        # Try different date formats
        date_formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%m-%d-%Y",
            "%m/%d/%y",
            "%d/%m/%Y",
            "%d-%m-%Y"
        ]
        
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(value, date_format)
                # Return in standard ISO format
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        # If no format matches, return original value
        return value
    
    def _clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and normalize parsed data.
        
        Args:
            data: Parsed data to clean
            
        Returns:
            Cleaned data
        """
        cleaned_data = {}
        
        for key, value in data.items():
            # Normalize field names (lowercase, replace spaces with underscores)
            clean_key = self._normalize_field_name(key)
            
            # Clean field values
            clean_value = self._clean_field_value(value)
            
            cleaned_data[clean_key] = clean_value
        
        return cleaned_data
    
    def _normalize_field_name(self, field_name: str) -> str:
        """
        Normalize field names to standard format.
        
        Args:
            field_name: Original field name
            
        Returns:
            Normalized field name
        """
        import re
        
        # Convert to lowercase
        normalized = field_name.lower()
        
        # Replace spaces and special characters with underscores
        normalized = re.sub(r'[^a-z0-9_]', '_', normalized)
        
        # Remove multiple consecutive underscores
        normalized = re.sub(r'_+', '_', normalized)
        
        # Remove leading/trailing underscores
        normalized = normalized.strip('_')
        
        return normalized
    
    def _clean_field_value(self, value: Any) -> Any:
        """
        Clean individual field values.
        
        Args:
            value: Field value to clean
            
        Returns:
            Cleaned field value
        """
        if isinstance(value, str):
            # Remove extra whitespace
            cleaned = value.strip()
            
            # Convert empty strings to None
            if cleaned == "":
                return None
            
            # Convert common null representations to None
            null_values = {"null", "none", "n/a", "na", "nil", "undefined"}
            if cleaned.lower() in null_values:
                return None
            
            return cleaned
        
        return value
    
    def get_parsing_statistics(self, original_data: Dict[str, Any], parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get statistics about the parsing process.
        
        Args:
            original_data: Original FAST UI data
            parsed_data: Parsed data
            
        Returns:
            Parsing statistics
        """
        stats = {
            "original_fields": len(original_data),
            "parsed_fields": len(parsed_data) - 1,  # Exclude metadata
            "field_type_distribution": {},
            "nested_sections": 0,
            "array_sections": 0
        }
        
        # Count field types in parsed data
        for key, value in parsed_data.items():
            if key == "_parsing_metadata":
                continue
                
            value_type = type(value).__name__
            stats["field_type_distribution"][value_type] = stats["field_type_distribution"].get(value_type, 0) + 1
        
        # Count nested and array sections in original data
        for value in original_data.values():
            if isinstance(value, dict):
                stats["nested_sections"] += 1
            elif isinstance(value, list):
                stats["array_sections"] += 1
        
        return stats


class ParsingError(Exception):
    """Exception raised when FAST UI parsing fails."""
    pass
