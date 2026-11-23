"""
Constants for configuration, suppression comments, file names and annotation inspection.

Read through linting_suite.config.constants, imported as const.
"""

from typing import Final, Literal

"Configuration defaults"

DEFAULT_MIN_DICT_KEYS: Final[int] = 3
DEFAULT_R003_MODE: Final[str] = "canonical"
DEFAULT_EXCEPTION_TAGS: Final[list[str]] = ["facade - celery schedule", "FRAMEWORK"]
DEFAULT_SERVICE_PATHS: Final[list[str]] = ["apps/*/services/*.py", "**/services/*.py"]
DEFAULT_DTO_PATHS: Final[list[str]] = ["**/dtos.py", "**/dtos/*.py"]
DEFAULT_R006_PATHS: Final[list[str]] = ["apps/*/services/*.py", "**/services/*.py"]
DEFAULT_R003_SENSITIVITY_BASES: Final[list[str]] = ["SensitiveRepr"]
DEFAULT_CONFIG_FILE: Final[str] = "pyproject.toml"


"Configuration sections and keys"

CONFIG_SECTION_STRICT_MODULE: Final[str] = "strict-module"
CONFIG_SECTION_DTO_STRICT: Final[str] = "dto-strict"
CONFIG_SECTION_LOC_CAP: Final[str] = "loc-cap"
CONFIG_ROOT_TOOL: Final[str] = "tool"
CONFIG_KEY_HARD_CAP: Final[str] = "hard_cap"
CONFIG_KEY_SOFT_TARGET: Final[str] = "soft_target"
CONFIG_KEY_BASELINE_FILE: Final[str] = "baseline_file"
CONFIG_KEY_SERVICE_PATHS: Final[str] = "service_paths"
CONFIG_KEY_DTO_PATHS: Final[str] = "dto_paths"
CONFIG_KEY_EXCEPTION_TAGS: Final[str] = "exception_tags"
CONFIG_KEY_DISABLED_RULES: Final[str] = "disabled_rules"
CONFIG_KEY_SEVERITY_OVERRIDES: Final[str] = "severity_overrides"
CONFIG_KEY_STRICT_COLLECTIONS: Final[str] = "strict_collections"
CONFIG_KEY_TAG_REQUIRES_JUSTIFICATION: Final[str] = "exception_tag_requires_justification"
CONFIG_KEY_MAX_TAGS_PER_FILE: Final[str] = "max_exception_tags_per_file"
CONFIG_KEY_R003_MODE: Final[str] = "r003_mode"
CONFIG_KEY_R006_PATHS: Final[str] = "r006_paths"
CONFIG_KEY_MIN_DICT_KEYS: Final[str] = "min_dict_keys"
CONFIG_KEY_R003_STRICT_REPR: Final[str] = "r003_strict_repr"
CONFIG_KEY_R003_SENSITIVITY_BASES: Final[str] = "r003_sensitivity_bases"
CONFIG_KEY_R003_SENSITIVITY_ALLOWLIST: Final[str] = "r003_sensitivity_allowlist"


"Suppression comments"

NOQA_KEYWORD: Final[str] = "noqa"
PREFIX_STRICT_MODULE: Final[str] = "strict-module"
PREFIX_DTO_STRICT: Final[str] = "dto-strict"
COMMENT_MARKER: Final[str] = "#"
NOQA_SPEC_SEPARATOR: Final[str] = ":"
NOQA_TOKEN_SEPARATOR: Final[str] = ","
NOQA_REASON_DASH: Final[str] = "-"
NOQA_REASON_DASHES: Final[str] = "-\u2013\u2014"
TEMPLATE_PREFIXED_RULE: Final[str] = "{prefix}-{rule_id}"
TAG_JUSTIFICATION_SEPARATOR: Final[str] = ":"


"File names and path patterns"

PY_EXTENSION: Final[str] = ".py"
BASENAME_CONSTANTS: Final[str] = "constants.py"
BASENAME_CONST_SUFFIX: Final[str] = "_const.py"
LOC_CAP_BASELINE_LEGACY_NAMES: Final[list[str]] = [".strict-module-baseline.txt", ".dto-strict-baseline.txt"]
DEFAULT_EXCLUDE_PATTERNS: Final[tuple[str, ...]] = ("migrations", "management/commands")
PY_GLOB: Final[str] = "*.py"
TEMPLATE_EXTENSION_GLOB: Final[str] = "*{extension}"
BASENAME_CONFTEST: Final[str] = "conftest.py"
TEST_FILE_PREFIX: Final[str] = "test_"
TESTS_DIRECTORY_INFIX: Final[str] = "/tests/"
TESTS_DIRECTORY_PREFIX: Final[str] = "tests/"
CONSTANTS_PATH_WORD: Final[str] = "constants"


"Annotation inspection"

BARE_COLLECTION_TYPES: Final[tuple[str, ...]] = ("dict", "list", "tuple")
DICT_STR_ANY_PATTERN: Final[str] = "dict[str,any]"
ANY_PATTERN: Final[str] = "any"
AST_INDEX_NODE: Final[str] = "Index"
ATTRIBUTE_LINENO: Final[Literal["lineno"]] = "lineno"
SPACE: Final[str] = " "
ELEMENT_SEPARATOR: Final[str] = ", "
TEMPLATE_SUBSCRIPT: Final[str] = "{base}[{index}]"
TEMPLATE_TUPLE: Final[str] = "({elements})"
TEMPLATE_ATTRIBUTE: Final[str] = "{value}.{attribute}"
