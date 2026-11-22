"""Rule registry for linting rules."""

from typing import Optional

import linting_suite.rules.rules_objects as objs


class RuleRegistry:
    """Registry of all linting rules."""

    RULES = {
        "R001": objs.Rule(
            "R001",
            "Dict[str, Any] or bare collections in service signatures",
            objs.RuleSeverity.HIGH,
            "Function signature contains Dict[str, Any], bare dict, list, or tuple without type parameters.",
        ),
        "R002": objs.Rule(
            "R002",
            "Inline dict literals with 3+ keys",
            objs.RuleSeverity.MEDIUM,
            "Inline dict literal with multiple string keys; consider converting to DTO.",
        ),
        "R003": objs.Rule(
            "R003",
            "Dataclass uses anti-canonical repr=False",
            objs.RuleSeverity.MEDIUM,
            "Dataclass uses anti-canonical repr=False. Per strict-module canonical (v0.2): plain @dataclass(frozen=True, slots=True). Remove repr=False.",
        ),
        "R004": objs.Rule(
            "R004",
            "Module-level function without exception tag",
            objs.RuleSeverity.HIGH,
            "Module-level function definition lacks documented exception tag (facade pattern).",
        ),
        "R005": objs.Rule(
            "R005",
            "Validator not using DTO.from_dict() pattern",
            objs.RuleSeverity.LOW,
            "Validator function should use DTO.from_dict() to validate payload shape.",
        ),
        "R006": objs.Rule(
            "R006",
            "typing.Any in signature",
            objs.RuleSeverity.HIGH,
            "Function signature contains typing.Any in parameter or return type. Use forward refs (TYPE_CHECKING) for class types, narrow protocols (IO[bytes]) for file objects, or build a proper DTO for business shapes.",
        ),
        "R007": objs.Rule(
            "R007",
            "Pytest fixtures defined outside conftest.py",
            objs.RuleSeverity.MEDIUM,
            "Pytest fixture @pytest.fixture decorator found in non-conftest file. Fixtures must be defined in conftest.py.",
        ),
        "R008": objs.Rule(
            "R008",
            "Bare module-level test function",
            objs.RuleSeverity.MEDIUM,
            "Module-level test function def test_*() found. Test functions must be defined as methods in Test<Concern> classes.",
        ),
        "R009": objs.Rule(
            "R009",
            "Module-level function outside allowed entry points",
            objs.RuleSeverity.HIGH,
            "Module-level function found in service path. All methods must be defined within classes. Allowed exceptions: main, handle_*, handle_command, handle_event, handle_request.",
        ),
        "R010": objs.Rule(
            "R010",
            "Legacy typing aliases for abstract base classes",
            objs.RuleSeverity.MEDIUM,
            "Import uses typing.* ABC alias instead of collections.abc. Typing aliases are deprecated since Python 3.9. Use collections.abc instead.",
        ),
        "R011": objs.Rule(
            "R011",
            "String literal at raise site",
            objs.RuleSeverity.HIGH,
            "Raise statement contains a string literal message. Extract to constants/<feature>.py as ERR_<DOMAIN>_<CONDITION>, reference via const.*.",
        ),
        "R012": objs.Rule(
            "R012",
            "Call fits on one line but is exploded (P3 amendment)",
            objs.RuleSeverity.INFO,
            "Multi-line call would fit within 100-char line length. Collapse to single line.",
        ),
        "R013": objs.Rule(
            "R013",
            "Signature grouping (P14 compact method signatures)",
            objs.RuleSeverity.INFO,
            "Multi-parameter signature should group 2-3 parameters per line, not one-per-line or 4+.",
        ),
        "R014": objs.Rule(
            "R014",
            "Kwarg-call grouping (P15 packed keyword groups)",
            objs.RuleSeverity.INFO,
            "Multi-kwarg call should group 2-3 kwargs per line, not one-per-line or 4+.",
        ),
        "R015": objs.Rule(
            "R015",
            "Wrap-path blank-line rhythm (P16 try/except symmetry)",
            objs.RuleSeverity.INFO,
            "Except block blank-line rhythm differs from try block. Mirror try's internal spacing.",
        ),
    }

    @classmethod
    def get_rule(cls, rule_id: str) -> Optional[objs.Rule]:
        """Get rule by ID."""
        return cls.RULES.get(rule_id)
