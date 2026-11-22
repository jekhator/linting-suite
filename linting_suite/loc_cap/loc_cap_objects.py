"""LOC cap configuration."""

from dataclasses import dataclass

import linting_suite.config.constants as const


@dataclass(frozen=True, slots=True)
class LocCapConfig:
    """Configuration for LOC cap checker."""

    hard_cap: int = const.DEFAULT_LOC_HARD_CAP
    soft_target: int = const.DEFAULT_LOC_SOFT_TARGET
    baseline_file: str = const.DEFAULT_LOC_CAP_BASELINE_FILE
    exclude_patterns: tuple[str, ...] = const.DEFAULT_EXCLUDE_PATTERNS
