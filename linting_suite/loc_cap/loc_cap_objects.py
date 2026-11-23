"""LOC cap configuration."""

from dataclasses import dataclass


class LocCapReadError(ValueError):
    """Error reading a file whose lines were to be counted."""


@dataclass(frozen=True, slots=True)
class LocCapConfig:
    """Configuration for LOC cap checker."""

    hard_cap: int = 694
    soft_target: int = 500
    baseline_file: str = ".loc-cap-baseline.txt"
    exclude_patterns: tuple[str, ...] = ("migrations", "management/commands")
