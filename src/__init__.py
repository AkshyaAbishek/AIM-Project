"""
AIM - Actuarial Input Mapper Package

A comprehensive solution for automating the mapping of FAST UI inputs
to product-specific actuarial calculation inputs.
"""

from .aim_processor import AIMProcessor, ValidationError, MappingError

__version__ = "1.0.0"
__author__ = "Actuarial Systems Team"

__all__ = [
    "AIMProcessor",
    "ValidationError", 
    "MappingError"
]
