"""Configuration module for strict-module."""

from linting_suite.config._config import Config, LocCapConfig
from linting_suite.config._version import __version__
from linting_suite.config.constants import *  # noqa: F401, F403

__all__ = ["Config", "LocCapConfig", "__version__"]
