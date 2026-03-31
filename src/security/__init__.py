"""
Security module for AI Procurement Readiness Tool

Provides:
- Reference document integrity verification (tamper detection)
- Input validation and sanitization (injection protection)
"""

from .security import (
    ReferenceDocumentVerifier,
    SecurityError,
    verify_reference_documents
)

from .input_validator import (
    InputValidator,
    ValidationError
)

__all__ = [
    'ReferenceDocumentVerifier',
    'SecurityError',
    'verify_reference_documents',
    'InputValidator',
    'ValidationError',
]

__version__ = '1.0.0'