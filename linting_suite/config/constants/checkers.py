"""
Constants for the checkers: violation messages and the names they look for.

Read through linting_suite.config.constants, imported as const.
"""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

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
