class DefinitionError(Exception):
	"""Base error for invalid inputs or generated definitions."""


class CatalogError(DefinitionError):
	"""Raised when the LibPinMAME catalog cannot be loaded or reconciled."""


class ValidationError(DefinitionError):
	"""Raised when a canonical artifact violates schema policy."""
