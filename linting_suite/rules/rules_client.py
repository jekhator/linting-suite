"""Rule registry for linting rules."""

from typing import Optional

import linting_suite.config.constants as const
from linting_suite.rules.rules_objects import Rule, RuleSeverity


class RuleRegistry:
    """Registry of all linting rules."""

    RULE_R001 = Rule(const.RULE_ID_R001, const.RULE_NAME_R001, RuleSeverity.HIGH, const.RULE_DESCRIPTION_R001)
    RULE_R002 = Rule(const.RULE_ID_R002, const.RULE_NAME_R002, RuleSeverity.MEDIUM, const.RULE_DESCRIPTION_R002)
    RULE_R003 = Rule(const.RULE_ID_R003, const.RULE_NAME_R003, RuleSeverity.MEDIUM, const.RULE_DESCRIPTION_R003)
    RULE_R004 = Rule(const.RULE_ID_R004, const.RULE_NAME_R004, RuleSeverity.HIGH, const.RULE_DESCRIPTION_R004)
    RULE_R005 = Rule(const.RULE_ID_R005, const.RULE_NAME_R005, RuleSeverity.LOW, const.RULE_DESCRIPTION_R005)
    RULE_R006 = Rule(const.RULE_ID_R006, const.RULE_NAME_R006, RuleSeverity.HIGH, const.RULE_DESCRIPTION_R006)
    RULE_R007 = Rule(const.RULE_ID_R007, const.RULE_NAME_R007, RuleSeverity.MEDIUM, const.RULE_DESCRIPTION_R007)
    RULE_R008 = Rule(const.RULE_ID_R008, const.RULE_NAME_R008, RuleSeverity.MEDIUM, const.RULE_DESCRIPTION_R008)
    RULE_R009 = Rule(const.RULE_ID_R009, const.RULE_NAME_R009, RuleSeverity.HIGH, const.RULE_DESCRIPTION_R009)
    RULE_R010 = Rule(const.RULE_ID_R010, const.RULE_NAME_R010, RuleSeverity.MEDIUM, const.RULE_DESCRIPTION_R010)
    RULE_R011 = Rule(const.RULE_ID_R011, const.RULE_NAME_R011, RuleSeverity.HIGH, const.RULE_DESCRIPTION_R011)
    RULE_R012 = Rule(const.RULE_ID_R012, const.RULE_NAME_R012, RuleSeverity.INFO, const.RULE_DESCRIPTION_R012)
    RULE_R013 = Rule(const.RULE_ID_R013, const.RULE_NAME_R013, RuleSeverity.INFO, const.RULE_DESCRIPTION_R013)
    RULE_R014 = Rule(const.RULE_ID_R014, const.RULE_NAME_R014, RuleSeverity.INFO, const.RULE_DESCRIPTION_R014)
    RULE_R015 = Rule(const.RULE_ID_R015, const.RULE_NAME_R015, RuleSeverity.INFO, const.RULE_DESCRIPTION_R015)
    RULES = {
        const.RULE_ID_R001: RULE_R001, const.RULE_ID_R002: RULE_R002, const.RULE_ID_R003: RULE_R003,
        const.RULE_ID_R004: RULE_R004, const.RULE_ID_R005: RULE_R005, const.RULE_ID_R006: RULE_R006,
        const.RULE_ID_R007: RULE_R007, const.RULE_ID_R008: RULE_R008, const.RULE_ID_R009: RULE_R009,
        const.RULE_ID_R010: RULE_R010, const.RULE_ID_R011: RULE_R011, const.RULE_ID_R012: RULE_R012,
        const.RULE_ID_R013: RULE_R013, const.RULE_ID_R014: RULE_R014, const.RULE_ID_R015: RULE_R015
    }

    @classmethod
    def get_rule(cls, rule_id: str) -> Optional[Rule]:
        """Get rule by ID."""
        return cls.RULES.get(rule_id)
