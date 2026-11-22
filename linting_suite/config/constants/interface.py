"""
Constants for output, exit codes, the baseline file, severity levels, the LOC cap and the command line.

Read through linting_suite.config.constants, imported as const.
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
