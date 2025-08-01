"""
Actuarial Input Builder - Main Module

This module provides the main interface for converting FAST UI inputs
to product-specific actuarial calculation inputs.
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .mappers.field_mapper import FieldMapper
from .validators.input_validator import InputValidator
from .parsers.fast_ui_parser import FastUIParser
from .config.config_manager import ConfigManager


class ActurialInputBuilder:
    """
    Main class for handling the conversion of FAST UI inputs to actuarial calculation inputs.
    
    This class orchestrates the entire process:
    1. Parse FAST UI input data
    2. Validate input according to business rules
    3. Map fields to actuarial calculation format
    4. Apply product-specific transformations
    5. Generate final output for actuarial calculations
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Actuarial Input Builder.
        
        Args:
            config_path (str, optional): Path to custom configuration file
        """
        self.config_manager = ConfigManager(config_path)
        self.parser = FastUIParser()
        self.validator = InputValidator(self.config_manager)
        self.mapper = FieldMapper(self.config_manager)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        
        self.logger.info("Actuarial Input Builder initialized")
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('actuarial_input_builder.log'),
                logging.StreamHandler()
            ]
        )
    
    def process_fast_ui_input(self, 
                            fast_ui_data: Dict[str, Any], 
                            product_type: str,
                            validation_level: str = "full") -> Dict[str, Any]:
        """
        Process FAST UI input data and convert to actuarial calculation format.
        
        Args:
            fast_ui_data (dict): Raw input data from FAST UI
            product_type (str): Type of insurance product (e.g., 'life', 'annuity', 'health')
            validation_level (str): Level of validation ('basic', 'full', 'strict')
        
        Returns:
            dict: Processed data ready for actuarial calculations
            
        Raises:
            ValidationError: If input data fails validation
            MappingError: If field mapping fails
        """
        start_time = datetime.now()
        self.logger.info(f"Starting processing for product type: {product_type}")
        
        try:
            # Step 1: Parse FAST UI data
            self.logger.info("Step 1: Parsing FAST UI data")
            parsed_data = self.parser.parse(fast_ui_data)
            self.logger.info(f"Parsed {len(parsed_data)} fields from FAST UI")
            
            # Step 2: Validate input data
            self.logger.info("Step 2: Validating input data")
            validation_result = self.validator.validate(parsed_data, product_type, validation_level)
            
            if not validation_result.is_valid:
                self.logger.error(f"Validation failed: {validation_result.errors}")
                raise ValidationError(validation_result.errors)
            
            self.logger.info("Input validation passed")
            
            # Step 3: Map fields to actuarial calculation format
            self.logger.info("Step 3: Mapping fields to actuarial format")
            mapped_data = self.mapper.map_fields(parsed_data, product_type)
            self.logger.info(f"Mapped to {len(mapped_data)} actuarial fields")
            
            # Step 4: Apply product-specific transformations
            self.logger.info("Step 4: Applying product-specific transformations")
            transformed_data = self._apply_transformations(mapped_data, product_type)
            
            # Step 5: Generate final output structure
            final_output = self._generate_output(transformed_data, product_type)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Processing completed successfully in {processing_time:.2f} seconds")
            
            return {
                "status": "success",
                "product_type": product_type,
                "processing_time": processing_time,
                "actuarial_inputs": final_output,
                "metadata": {
                    "processed_at": datetime.now().isoformat(),
                    "validation_level": validation_level,
                    "fields_processed": len(parsed_data),
                    "fields_mapped": len(mapped_data)
                }
            }
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Processing failed after {processing_time:.2f} seconds: {str(e)}")
            
            return {
                "status": "error",
                "error_message": str(e),
                "product_type": product_type,
                "processing_time": processing_time,
                "processed_at": datetime.now().isoformat()
            }
    
    def _apply_transformations(self, mapped_data: Dict[str, Any], product_type: str) -> Dict[str, Any]:
        """
        Apply product-specific transformations to mapped data.
        
        Args:
            mapped_data (dict): Data after field mapping
            product_type (str): Product type for transformation rules
            
        Returns:
            dict: Transformed data
        """
        transformations = self.config_manager.get_transformations(product_type)
        transformed_data = mapped_data.copy()
        
        for transformation in transformations:
            field_name = transformation.get("field")
            transform_type = transformation.get("type")
            
            if field_name in transformed_data:
                if transform_type == "currency_conversion":
                    transformed_data[field_name] = self._convert_currency(
                        transformed_data[field_name], 
                        transformation.get("from_currency", "USD"),
                        transformation.get("to_currency", "USD")
                    )
                elif transform_type == "date_format":
                    transformed_data[field_name] = self._format_date(
                        transformed_data[field_name],
                        transformation.get("format", "%Y-%m-%d")
                    )
                elif transform_type == "calculation":
                    transformed_data[field_name] = self._apply_calculation(
                        transformed_data,
                        transformation.get("formula")
                    )
        
        return transformed_data
    
    def _convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert currency amounts (placeholder implementation)."""
        # In a real implementation, this would use actual exchange rates
        if from_currency == to_currency:
            return amount
        
        # Placeholder conversion rates
        rates = {"USD": 1.0, "EUR": 0.85, "GBP": 0.73}
        usd_amount = amount / rates.get(from_currency, 1.0)
        return usd_amount * rates.get(to_currency, 1.0)
    
    def _format_date(self, date_value: Any, date_format: str) -> str:
        """Format date values according to specified format."""
        if isinstance(date_value, str):
            try:
                # Try to parse the date and reformat it
                parsed_date = datetime.strptime(date_value, "%Y-%m-%d")
                return parsed_date.strftime(date_format)
            except ValueError:
                return date_value
        return str(date_value)
    
    def _apply_calculation(self, data: Dict[str, Any], formula: str) -> float:
        """Apply calculation formula to data fields."""
        # Simple formula evaluation (in production, use a safer approach)
        try:
            # Replace field names in formula with actual values
            for field_name, value in data.items():
                if isinstance(value, (int, float)):
                    formula = formula.replace(f"{{{field_name}}}", str(value))
            
            # Evaluate the formula (use ast.literal_eval or safer methods in production)
            result = eval(formula)
            return float(result)
        except Exception:
            self.logger.warning(f"Failed to evaluate formula: {formula}")
            return 0.0
    
    def _generate_output(self, transformed_data: Dict[str, Any], product_type: str) -> Dict[str, Any]:
        """
        Generate the final output structure for actuarial calculations.
        
        Args:
            transformed_data (dict): Transformed and mapped data
            product_type (str): Product type for output structure
            
        Returns:
            dict: Final output structure
        """
        output_template = self.config_manager.get_output_template(product_type)
        
        final_output = {}
        
        for section_name, section_config in output_template.items():
            final_output[section_name] = {}
            
            for field_name in section_config.get("fields", []):
                if field_name in transformed_data:
                    final_output[section_name][field_name] = transformed_data[field_name]
                else:
                    # Use default value if field is missing
                    default_value = section_config.get("defaults", {}).get(field_name)
                    if default_value is not None:
                        final_output[section_name][field_name] = default_value
        
        return final_output
    
    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate the current configuration setup.
        
        Returns:
            dict: Validation results for configuration
        """
        return self.config_manager.validate_configuration()
    
    def get_supported_products(self) -> list:
        """
        Get list of supported product types.
        
        Returns:
            list: List of supported product types
        """
        return self.config_manager.get_supported_products()


class ValidationError(Exception):
    """Exception raised when input validation fails."""
    pass


class MappingError(Exception):
    """Exception raised when field mapping fails."""
    pass
