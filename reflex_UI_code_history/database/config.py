from __future__ import annotations

"""Deprecated local DBConfig shim.

This module now re-exports DBConfig from the central configs package to
keep backward compatibility while centralizing configuration.
"""

# Re-export the centralized DBConfig
from configs import DBConfig  # noqa: F401
