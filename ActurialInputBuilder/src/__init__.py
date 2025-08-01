"""
Actuarial Input Builder Package

A comprehensive solution for automating the mapping of FAST UI inputs
to product-specific actuarial calculation inputs.
"""

from .input_builder import ActurialInputBuilder, ValidationError, MappingError

__version__ = "1.0.0"
__author__ = "Actuarial Systems Team"

__all__ = [
    "ActurialInputBuilder",
    "ValidationError", 
    "MappingError"
]
