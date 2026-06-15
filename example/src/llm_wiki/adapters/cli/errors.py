"""Configuration adapter errors (S3)."""

from __future__ import annotations


class VaultNotFoundError(Exception):
    """Raised when walk-up and --vault both fail (S3)."""


class ConfigurationError(Exception):
    """Raised for invalid CLI or environment configuration."""
