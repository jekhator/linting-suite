"""
Constants for the rule registry: ids, names and descriptions.

Read through linting_suite.config.constants, imported as const.
"""

from typing import Final

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
