"""
Configuration constants and fixed strings for strict-module.

Imported as const.
"""

from typing import Final

"Output formats and rendering"

FORMAT_TEXT: Final[str] = "text"
FORMAT_GITHUB: Final[str] = "github"
FORMAT_JSON: Final[str] = "json"
VALID_FORMATS: Final[list[str]] = [FORMAT_TEXT, FORMAT_GITHUB, FORMAT_JSON]
GITHUB_LEVEL_ERROR: Final[str] = "error"
GITHUB_LEVEL_NOTICE: Final[str] = "notice"
GITHUB_LEVEL_WARNING: Final[str] = "warning"


"Exit codes"

EXIT_CODE_SUCCESS: Final[int] = 0
EXIT_CODE_HIGH_VIOLATION: Final[int] = 1
EXIT_CODE_MEDIUM_VIOLATION: Final[int] = 2
EXIT_CODE_LOW_VIOLATION: Final[int] = 3


"Baseline file"

ERR_NONEXISTENT_PATH: Final[str] = "error: path does not exist: {path}"
ERR_BASELINE_MISSING: Final[str] = "error: baseline file not found or unreadable: {path}"
ERR_BASELINE_INVALID_JSON: Final[str] = "error: baseline file contains invalid JSON: {path}"
ERR_BASELINE_NOT_LIST: Final[str] = "error: baseline file top level must be a list: {path}"
ERR_BASELINE_ENTRY_NOT_OBJECT: Final[str] = "error: baseline entry {index} is not an object: {path}"
ERR_BASELINE_ENTRY_SHAPE: Final[str] = "error: baseline entry {index} is missing required key '{key}': {path}"
MSG_BASELINE_LOADED: Final[str] = "baseline: {count} entries loaded from {path}"
REQUIRED_BASELINE_KEYS: Final[tuple[str, ...]] = ("file", "line", "rule_id", "message_hash")


"Severity levels"

VALID_SEVERITY_LEVELS: Final[list[str]] = ["HIGH", "MEDIUM", "LOW", "INFO"]


"LOC cap"

DEFAULT_LOC_HARD_CAP: Final[int] = 694
DEFAULT_LOC_SOFT_TARGET: Final[int] = 500
DEFAULT_LOC_CAP_BASELINE_FILE: Final[str] = ".loc-cap-baseline.txt"


"Configuration defaults"

DEFAULT_MIN_DICT_KEYS: Final[int] = 3
DEFAULT_R003_MODE: Final[str] = "canonical"
DEFAULT_EXCEPTION_TAGS: Final[list[str]] = ["facade - celery schedule", "FRAMEWORK"]
DEFAULT_SERVICE_PATHS: Final[list[str]] = ["apps/*/services/*.py", "**/services/*.py"]
DEFAULT_DTO_PATHS: Final[list[str]] = ["**/dtos.py", "**/dtos/*.py"]
DEFAULT_R006_PATHS: Final[list[str]] = ["apps/*/services/*.py", "**/services/*.py"]


"Configuration sections and keys"

CONFIG_SECTION_STRICT_MODULE: Final[str] = "strict-module"
CONFIG_SECTION_DTO_STRICT: Final[str] = "dto-strict"
CONFIG_SECTION_LOC_CAP: Final[str] = "loc-cap"


"Suppression comments"

NOQA_KEYWORD: Final[str] = "noqa"
PREFIX_STRICT_MODULE: Final[str] = "strict-module"
PREFIX_DTO_STRICT: Final[str] = "dto-strict"


"File names and path patterns"

PY_EXTENSION: Final[str] = ".py"
BASENAME_CONSTANTS: Final[str] = "constants.py"
BASENAME_CONST_SUFFIX: Final[str] = "_const.py"
LOC_CAP_BASELINE_LEGACY_NAMES: Final[list[str]] = [".strict-module-baseline.txt", ".dto-strict-baseline.txt"]
DEFAULT_EXCLUDE_PATTERNS: Final[tuple[str, ...]] = ("migrations", "management/commands")


"Annotation inspection"

BARE_COLLECTION_TYPES: Final[tuple[str, ...]] = ("dict", "list", "tuple")
DICT_STR_ANY_PATTERN: Final[str] = "dict[str,any]"
