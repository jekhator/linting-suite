"""
Configuration constants and fixed strings for strict-module.

Imported as const.
"""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final, Literal

"Output formats and rendering"

FORMAT_TEXT: Final[str] = "text"
FORMAT_GITHUB: Final[str] = "github"
FORMAT_JSON: Final[str] = "json"
VALID_FORMATS: Final[list[str]] = [FORMAT_TEXT, FORMAT_GITHUB, FORMAT_JSON]
GITHUB_LEVEL_ERROR: Final[str] = "error"
GITHUB_LEVEL_NOTICE: Final[str] = "notice"
GITHUB_LEVEL_WARNING: Final[str] = "warning"
TEMPLATE_VIOLATION_TEXT: Final[str] = "{file}:{line}: {rule_id} {message}"
TEMPLATE_VIOLATION_GITHUB: Final[str] = "::{level} file={file},line={line},col={col}::{message}"
VIOLATION_KEY_RULE_ID: Final[str] = "rule_id"
VIOLATION_KEY_SEVERITY: Final[str] = "severity"
VIOLATION_KEY_FILE: Final[str] = "file"
VIOLATION_KEY_LINE: Final[str] = "line"
VIOLATION_KEY_COL: Final[str] = "col"
VIOLATION_KEY_MESSAGE: Final[str] = "message"
JSON_INDENT: Final[int] = 2
LINE_SEPARATOR: Final[str] = "\n"


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
BASELINE_KEY_FILE: Final[str] = "file"
BASELINE_KEY_LINE: Final[str] = "line"
BASELINE_KEY_RULE_ID: Final[str] = "rule_id"
BASELINE_KEY_MESSAGE_HASH: Final[str] = "message_hash"
MESSAGE_HASH_LENGTH: Final[int] = 16
FILE_MODE_READ: Final[str] = "r"
FILE_MODE_READ_BINARY: Final[str] = "rb"
ENCODING_UTF8: Final[str] = "utf-8"


"Severity levels"

SEVERITY_HIGH: Final[str] = "HIGH"
SEVERITY_MEDIUM: Final[str] = "MEDIUM"
SEVERITY_LOW: Final[str] = "LOW"
SEVERITY_INFO: Final[str] = "INFO"
VALID_SEVERITY_LEVELS: Final[list[str]] = ["HIGH", "MEDIUM", "LOW", "INFO"]


"LOC cap"

DEFAULT_LOC_HARD_CAP: Final[int] = 694
DEFAULT_LOC_SOFT_TARGET: Final[int] = 500
DEFAULT_LOC_CAP_BASELINE_FILE: Final[str] = ".loc-cap-baseline.txt"
LOC_BASELINE_SEPARATOR: Final[str] = ":"
LOC_BASELINE_PARTS: Final[int] = 2
TEMPLATE_LOC_BASELINE_LINE: Final[str] = "{path}:{loc}"
MSG_LOC_SOFT_ENTRY: Final[str] = "  {loc}  {path}"
MSG_LOC_NEW_OFFENDER: Final[str] = "  {loc}  {path} (NEW OFFENDER)"
MSG_LOC_GREW: Final[str] = "  {loc}  {path} (was {baseline}, grew by {delta})"
MSG_LOC_DELETED: Final[str] = "  {path} (deleted)"
MSG_LOC_IMPROVED: Final[str] = "  {loc}  {path} (was {baseline}, improved by {delta})"
MSG_LOC_SOFT_HEADER: Final[str] = "::warning::Files over soft target ({soft_target} LOC) - consider decomposition:"
MSG_LOC_IMPROVED_HEADER: Final[str] = "::notice::Files improved (under {hard_cap} LOC):"
MSG_LOC_HARD_HEADER: Final[str] = "::error::Files exceed hard cap of {hard_cap} LOC. Decompose by cohesion:"
MSG_LOC_RATIONALE: Final[str] = "See memory/feedback_dto_refactor_autonomous_priority.md for cap rationale."
MSG_LOC_TESTS: Final[str] = "Tests: cap applies. Decompose by class-under-test; lift fixtures to conftest if needed."
MSG_LOC_REFACTOR: Final[str] = (
    "Refactor approach: split by COHESION not line count. E.g., bedrock.py -> bedrock/{invoke,embed,dtos}.py"
)
MSG_LOC_WITHIN_CAP: Final[str] = (
    "\u2713 All Python files within {hard_cap} LOC cap (ratchet: baseline allows improvements)"
)


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


"Command line"

CLI_SUBCOMMAND_LOC_CAP: Final[str] = "loc-cap"
CLI_PROG_LOC_CAP: Final[str] = "dto-strict loc-cap"
CLI_DESCRIPTION_LOC_CAP: Final[str] = "LOC cap enforcer with configurable hard/soft limits and ratchet baseline."
CLI_DESCRIPTION: Final[str] = "AST-based linter for Python DTO discipline and facade-ban enforcement."
CLI_ARG_PATH: Final[str] = "path"
CLI_FLAG_CONFIG: Final[str] = "--config"
CLI_FLAG_HARD_CAP: Final[str] = "--hard-cap"
CLI_FLAG_SOFT_TARGET: Final[str] = "--soft-target"
CLI_FLAG_BASELINE: Final[str] = "--baseline"
CLI_FLAG_GENERATE_BASELINE: Final[str] = "--generate-baseline"
CLI_FLAG_FORMAT: Final[str] = "--format"
CLI_ACTION_STORE_TRUE: Final[str] = "store_true"
CLI_NARGS_ANY: Final[str] = "*"
CLI_ARGUMENTS_OFFSET: Final[int] = 2
CLI_HELP_LOC_PATH: Final[str] = "Path to directory to scan"
CLI_HELP_CONFIG: Final[str] = "Path to pyproject.toml config file (default: pyproject.toml)"
CLI_HELP_HARD_CAP: Final[str] = (
    f"Hard cap limit (default: {DEFAULT_LOC_HARD_CAP}, or from [tool.strict-module.loc-cap].hard_cap)"
)
CLI_HELP_SOFT_TARGET: Final[str] = (
    f"Soft target limit (default: {DEFAULT_LOC_SOFT_TARGET}, or from [tool.strict-module.loc-cap].soft_target)"
)
CLI_HELP_LOC_BASELINE: Final[str] = (
    f"Baseline file path (default: {DEFAULT_LOC_CAP_BASELINE_FILE}, or from "
    "[tool.strict-module.loc-cap].baseline_file)"
)
CLI_HELP_LOC_GENERATE_BASELINE: Final[str] = "Generate baseline from all Python files in path (stdout)"
CLI_HELP_PATH: Final[str] = "Path(s) to file or directory to lint"
CLI_HELP_FORMAT: Final[str] = f"Output format (default: {FORMAT_TEXT})"
CLI_HELP_GENERATE_BASELINE: Final[str] = "Generate baseline JSON from all violations in path and output to stdout"
CLI_HELP_BASELINE: Final[str] = "Path to baseline JSON file; violations in baseline are accepted (ratchet mode)"
ERR_GENERATE_BASELINE_REQUIRES_PATH: Final[str] = "error: --generate-baseline requires PATH argument"
ERR_PATH_REQUIRED: Final[str] = "error: PATH argument required (unless using --generate-baseline)"


"Rule ids"

RULE_ID_R001: Final[str] = "R001"
RULE_ID_R002: Final[str] = "R002"
RULE_ID_R003: Final[str] = "R003"
RULE_ID_R004: Final[str] = "R004"
RULE_ID_R005: Final[str] = "R005"
RULE_ID_R006: Final[str] = "R006"
RULE_ID_R007: Final[str] = "R007"
RULE_ID_R008: Final[str] = "R008"
RULE_ID_R009: Final[str] = "R009"
RULE_ID_R010: Final[str] = "R010"
RULE_ID_R011: Final[str] = "R011"
RULE_ID_R012: Final[str] = "R012"
RULE_ID_R013: Final[str] = "R013"
RULE_ID_R014: Final[str] = "R014"
RULE_ID_R015: Final[str] = "R015"


"Rule names"

RULE_NAME_R001: Final[str] = "Dict[str, Any] or bare collections in service signatures"
RULE_NAME_R002: Final[str] = "Inline dict literals with 3+ keys"
RULE_NAME_R003: Final[str] = "Dataclass uses anti-canonical repr=False"
RULE_NAME_R004: Final[str] = "Module-level function without exception tag"
RULE_NAME_R005: Final[str] = "Validator not using DTO.from_dict() pattern"
RULE_NAME_R006: Final[str] = "typing.Any in signature"
RULE_NAME_R007: Final[str] = "Pytest fixtures defined outside conftest.py"
RULE_NAME_R008: Final[str] = "Bare module-level test function"
RULE_NAME_R009: Final[str] = "Module-level function outside allowed entry points"
RULE_NAME_R010: Final[str] = "Legacy typing aliases for abstract base classes"
RULE_NAME_R011: Final[str] = "String literal at raise site"
RULE_NAME_R012: Final[str] = "Call fits on one line but is exploded (P3 amendment)"
RULE_NAME_R013: Final[str] = "Signature grouping (P14 compact method signatures)"
RULE_NAME_R014: Final[str] = "Kwarg-call grouping (P15 packed keyword groups)"
RULE_NAME_R015: Final[str] = "Wrap-path blank-line rhythm (P16 try/except symmetry)"


"Rule descriptions"

RULE_DESCRIPTION_R001: Final[str] = (
    "Function signature contains Dict[str, Any], bare dict, list, or tuple without type parameters."
)
RULE_DESCRIPTION_R002: Final[str] = "Inline dict literal with multiple string keys; consider converting to DTO."
RULE_DESCRIPTION_R003: Final[str] = (
    "Dataclass uses anti-canonical repr=False. Per strict-module canonical (v0.2): plain @dataclass(frozen=True, "
    "slots=True). Remove repr=False."
)
RULE_DESCRIPTION_R004: Final[str] = "Module-level function definition lacks documented exception tag (facade pattern)."
RULE_DESCRIPTION_R005: Final[str] = "Validator function should use DTO.from_dict() to validate payload shape."
RULE_DESCRIPTION_R006: Final[str] = (
    "Function signature contains typing.Any in parameter or return type. Use forward refs (TYPE_CHECKING) for class "
    "types, narrow protocols (IO[bytes]) for file objects, or build a proper DTO for business shapes."
)
RULE_DESCRIPTION_R007: Final[str] = (
    "Pytest fixture @pytest.fixture decorator found in non-conftest file. Fixtures must be defined in conftest.py."
)
RULE_DESCRIPTION_R008: Final[str] = (
    "Module-level test function def test_*() found. Test functions must be defined as methods in Test<Concern> "
    "classes."
)
RULE_DESCRIPTION_R009: Final[str] = (
    "Module-level function found in service path. All methods must be defined within classes. Allowed exceptions: "
    "main, handle_*, handle_command, handle_event, handle_request."
)
RULE_DESCRIPTION_R010: Final[str] = (
    "Import uses typing.* ABC alias instead of collections.abc. Typing aliases are deprecated since Python 3.9. Use "
    "collections.abc instead."
)
RULE_DESCRIPTION_R011: Final[str] = (
    "Raise statement contains a string literal message. Extract to constants/<feature>.py as ERR_<DOMAIN>_<CONDITION>, "
    "reference via const.*."
)
RULE_DESCRIPTION_R012: Final[str] = "Multi-line call would fit within 100-char line length. Collapse to single line."
RULE_DESCRIPTION_R013: Final[str] = (
    "Multi-parameter signature should group 2-3 parameters per line, not one-per-line or 4+."
)
RULE_DESCRIPTION_R014: Final[str] = "Multi-kwarg call should group 2-3 kwargs per line, not one-per-line or 4+."
RULE_DESCRIPTION_R015: Final[str] = (
    "Except block blank-line rhythm differs from try block. Mirror try's internal spacing."
)


"Violation messages"

MSG_R001_DICT_STR_ANY: Final[str] = "Dict[str, Any] in signature: {name}"
MSG_R001_BARE_COLLECTION: Final[str] = (
    "Bare collection type in signature: {name} (use strict_collections=False to disable)"
)
MSG_R002_MISSING_JUSTIFICATION: Final[str] = (
    "Exception tag missing justification. Format: 'tag: explanation' (e.g., 'facade - celery schedule: transient event "
    "payload')"
)
MSG_R002_TAG_LIMIT: Final[str] = "Exceeded max exception tags ({limit}) in file"
MSG_R002_INLINE_DICT: Final[str] = "Inline dict literal with {count} keys (likely business-shape; convert to DTO)"
MSG_R003_REPR_FALSE: Final[str] = "@dataclass uses anti-canonical repr=False: {name}. Remove it."
MSG_R003_MISSING: Final[str] = "@dataclass missing {missing}: {name}"
ERR_R003_ALLOWLIST_UNDETECTED: Final[str] = (
    "Class {class_name} is in r003_sensitivity_allowlist but no sensitivity base or field metadata detected. Config "
    "may be stale."
)
MSG_R004_NO_TAG: Final[str] = "Module-level def without exception tag: {name}"
MSG_R005_NO_FROM_DICT: Final[str] = "Validator does not use DTO.from_dict() pattern: {name}"
MSG_R006_PARAMETER: Final[str] = "typing.Any in parameter: {name}"
MSG_R006_VARARGS: Final[str] = "typing.Any in *args: {name}"
MSG_R006_KWARGS: Final[str] = "typing.Any in **kwargs: {name}"
MSG_R006_RETURN: Final[str] = "typing.Any in return type: {name}"
MSG_R007_FIXTURE: Final[str] = "Pytest fixture defined outside conftest.py: {name}. Move to conftest.py."
MSG_R008_TEST_FUNCTION: Final[str] = "Module-level test function: {name}. Move into Test<Concern> class."
MSG_R009_MODULE_FUNCTION: Final[str] = (
    "Module-level function '{name}' found in service path. Every method must be in a class. Allowed exceptions: "
    "{allowed}."
)
MSG_R010_LEGACY_IMPORT: Final[str] = (
    "Import '{name}' from typing, not collections.abc. Use 'from collections.abc import {name}' instead."
)
MSG_R011_RAISE_LITERAL: Final[str] = (
    "String literal found in raise statement. Extract to constants/<feature>.py as ERR_<DOMAIN>_<CONDITION>, reference "
    "via const."
)
MSG_R012_SINGLE_ARGUMENT: Final[str] = "Single-argument call unnecessarily split across lines. Keep on one line."
MSG_R013_HANDLER_LINE: Final[str] = "Handler signature line has {count} params (>5). Group 2-5 per line."
MSG_R014_PACK: Final[str] = "Log event call: pack maximum 3 kwargs per line (found {count})."
MSG_R014_EXPLODE: Final[str] = "Log event call 2-3 kwargs: FULL-EXPLODE one-per-line."
MSG_R015_GROUPS: Final[str] = "{leg} leg: statement groups must be separated by EXACTLY one blank line."
MSG_R015_TIMING: Final[str] = (
    "Timing-capture pair (perf_counter + latency calc) must be contiguous (no blank lines within)."
)


"Checker vocabulary"

DECORATOR_DATACLASS: Final[str] = "dataclass"
DECORATOR_CLASSMETHOD: Final[str] = "classmethod"
DECORATOR_FIXTURE: Final[str] = "fixture"
MODULE_PYTEST: Final[str] = "pytest"
MODULE_TYPING: Final[str] = "typing"
SERIALIZER_PREFIX: Final[str] = "to_"
VALIDATOR_PREFIX: Final[str] = "validate_"
TEST_FUNCTION_PREFIX: Final[str] = "test_"
HANDLER_PREFIX: Final[str] = "handle_"
HANDLER_WILDCARD: Final[str] = "handle_*"
R009_ALLOWED_ENTRY_POINTS: Final[tuple[str, ...]] = ("main", "handle_command", "handle_event", "handle_request")
PARAMETER_PAYLOAD: Final[str] = "payload"
METHOD_FROM_DICT: Final[str] = "from_dict"
VALIDATION_ERROR_NAME: Final[str] = "ValidationError"
R003_MODE_CANONICAL: Final[str] = "canonical"
DATACLASS_KWARG_REPR: Final[str] = "repr"
DATACLASS_KWARG_FROZEN: Final[str] = "frozen"
DATACLASS_KWARG_SLOTS: Final[str] = "slots"
LITERAL_TRUE: Final[str] = "True"
LITERAL_FALSE: Final[str] = "False"
DATACLASS_FROZEN_TRUE: Final[str] = "frozen=True"
DATACLASS_SLOTS_TRUE: Final[str] = "slots=True"
DATACLASS_REPR_FALSE: Final[str] = "repr=False"
FUNCTION_FIELD: Final[str] = "field"
FIELD_KWARG_METADATA: Final[str] = "metadata"
METADATA_KEY_SENSITIVITY: Final[str] = "sensitivity"
TEMPLATE_CLASS_PATH: Final[str] = "{module}.{name}"
R012_MIN_LINE_SPAN: Final[int] = 2
R012_MAX_ONE_LINE_LENGTH: Final[int] = 80
QUOTE_CHARACTERS: Final[tuple[str, ...]] = ('"', "'")
ESCAPE_CHARACTER: Final[str] = "\\"
R013_MIN_PARAMETERS: Final[int] = 3
R013_MAX_PARAMETERS_PER_LINE: Final[int] = 5
R013_HANDLER_PREFIX_LOG: Final[str] = "log_"
R013_HANDLER_PREFIX_RECORD: Final[str] = "record_"
R013_HANDLER_PREFIX_WRAP: Final[str] = "wrap_"
R014_MIN_KWARGS: Final[int] = 2
R014_PACK_MIN_KWARGS: Final[int] = 4
R014_MAX_KWARGS_PER_LINE: Final[int] = 3
R014_EXPLODE_KWARG_COUNTS: Final[tuple[int, ...]] = (2, 3)
LOG_METHOD_PREFIX: Final[str] = "log"
LOG_EVENT_MARKER: Final[str] = "LOG_EVENT"
KWARG_SPREAD_LABEL: Final[str] = "**kwarg"
LEG_TRY: Final[str] = "try"
LEG_EXCEPT: Final[str] = "except"
R015_MAX_GROUP_GAP: Final[int] = 2
TIMING_TARGET_MARKER: Final[str] = "latency"
TIMING_CLOCK_NAME: Final[str] = "perf_counter"
FUNCTION_ROUND: Final[str] = "round"


"Legacy typing aliases"

R010_LEGACY_TO_MODERN: Final[Mapping[str, str]] = MappingProxyType(
    {
        "Callable": "collections.abc.Callable", "Iterable": "collections.abc.Iterable",
        "Iterator": "collections.abc.Iterator", "Awaitable": "collections.abc.Awaitable",
        "AsyncIterable": "collections.abc.AsyncIterable", "AsyncIterator": "collections.abc.AsyncIterator",
        "Mapping": "collections.abc.Mapping", "MutableMapping": "collections.abc.MutableMapping",
        "Sequence": "collections.abc.Sequence", "MutableSequence": "collections.abc.MutableSequence",
        "Set": "collections.abc.Set", "MutableSet": "collections.abc.MutableSet",
        "Hashable": "collections.abc.Hashable", "Sized": "collections.abc.Sized",
        "Container": "collections.abc.Container", "Collection": "collections.abc.Collection",
        "Reversible": "collections.abc.Reversible", "Generator": "collections.abc.Generator",
        "AsyncGenerator": "collections.abc.AsyncGenerator", "Coroutine": "collections.abc.Coroutine"
    }
)
