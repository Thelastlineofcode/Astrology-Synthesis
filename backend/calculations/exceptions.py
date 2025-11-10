"""
Custom exceptions for the calculation engine.

This module defines domain-specific exceptions for better error handling
and clearer error messages throughout the astrological calculation system.
"""


class CalculationError(Exception):
    """Base exception for all calculation-related errors."""
    pass


class InvalidBirthDataError(CalculationError):
    """Raised when birth data is invalid or incomplete."""
    pass


class InvalidDateRangeError(CalculationError):
    """Raised when date range is invalid (e.g., start > end)."""
    pass


class InvalidLongitudeError(CalculationError):
    """Raised when a longitude value is out of valid range (0-360)."""
    pass


class InvalidLatitudeError(CalculationError):
    """Raised when a latitude value is out of valid range (-90 to +90)."""
    pass


class PlanetNotFoundError(CalculationError):
    """Raised when a requested planet is not recognized."""
    pass


class HouseCalculationError(CalculationError):
    """Raised when house cusp calculation fails."""
    pass


class DashaCalculationError(CalculationError):
    """Raised when dasha period calculation fails."""
    pass


class EphemerisError(CalculationError):
    """Raised when ephemeris calculation fails."""
    pass


class InvalidPredictionWindowError(CalculationError):
    """Raised when prediction window parameters are invalid."""
    pass


class SignificatorError(CalculationError):
    """Raised when significator analysis fails."""
    pass


class TransitCalculationError(CalculationError):
    """Raised when transit calculation fails."""
    pass


class InterpretationError(CalculationError):
    """Raised when interpretation generation fails."""
    pass
