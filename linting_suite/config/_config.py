"""Configuration loading for strict-module (formerly dto-strict)."""

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

import linting_suite.config.constants as const


@dataclass(frozen=True, slots=True)
class LocCapConfig:
    """Configuration for LOC cap checker."""

    hard_cap: int = const.DEFAULT_LOC_HARD_CAP
    soft_target: int = const.DEFAULT_LOC_SOFT_TARGET
    baseline_file: str = const.DEFAULT_LOC_CAP_BASELINE_FILE


@dataclass(frozen=True, slots=True)
class Config:
    """Configuration for strict-module linter."""

    service_paths: list[str] = field(
        default_factory=lambda: const.DEFAULT_SERVICE_PATHS.copy()
    )
    dto_paths: list[str] = field(default_factory=lambda: const.DEFAULT_DTO_PATHS.copy())
    exception_tags: list[str] = field(
        default_factory=lambda: const.DEFAULT_EXCEPTION_TAGS.copy()
    )
    disabled_rules: list[str] = field(default_factory=list)
    severity_overrides: dict[str, str] = field(default_factory=dict)
    strict_collections: bool = field(default=False)
    exception_tag_requires_justification: bool = field(default=False)
    max_exception_tags_per_file: int | None = field(default=None)
    r003_mode: str = field(default=const.DEFAULT_R003_MODE)
    r006_paths: list[str] = field(default_factory=lambda: const.DEFAULT_R006_PATHS.copy())
    min_dict_keys: int = field(default=const.DEFAULT_MIN_DICT_KEYS)
    r003_strict_repr: bool = field(default=True)
    r003_sensitivity_bases: list[str] = field(default_factory=lambda: const.DEFAULT_R003_SENSITIVITY_BASES.copy())
    r003_sensitivity_allowlist: list[str] = field(default_factory=list)
    loc_cap: LocCapConfig = field(default_factory=LocCapConfig)

    @classmethod
    def from_pyproject(cls, path: Path) -> Self:
        """Load configuration from pyproject.toml."""
        if not path.exists():
            return cls()

        try:
            with open(path, const.FILE_MODE_READ_BINARY) as handle:
                data = tomllib.load(handle)
        except Exception:
            return cls()

        tool_data = data.get(const.CONFIG_ROOT_TOOL, {})
        config_data = tool_data.get(const.CONFIG_SECTION_STRICT_MODULE) or tool_data.get(
            const.CONFIG_SECTION_DTO_STRICT, {}
        )
        loc_cap_data = config_data.get(const.CONFIG_SECTION_LOC_CAP, {})

        hard_cap = loc_cap_data.get(const.CONFIG_KEY_HARD_CAP, const.DEFAULT_LOC_HARD_CAP)
        soft_target = loc_cap_data.get(const.CONFIG_KEY_SOFT_TARGET, const.DEFAULT_LOC_SOFT_TARGET)
        baseline_file = loc_cap_data.get(const.CONFIG_KEY_BASELINE_FILE, const.DEFAULT_LOC_CAP_BASELINE_FILE)
        loc_cap = LocCapConfig(
            hard_cap=hard_cap,
            soft_target=soft_target,
            baseline_file=baseline_file,
        )

        service_paths = config_data.get(const.CONFIG_KEY_SERVICE_PATHS, const.DEFAULT_SERVICE_PATHS)
        dto_paths = config_data.get(const.CONFIG_KEY_DTO_PATHS, const.DEFAULT_DTO_PATHS)
        exception_tags = config_data.get(const.CONFIG_KEY_EXCEPTION_TAGS, const.DEFAULT_EXCEPTION_TAGS)
        disabled_rules = config_data.get(const.CONFIG_KEY_DISABLED_RULES, [])
        severity_overrides = config_data.get(const.CONFIG_KEY_SEVERITY_OVERRIDES, {})
        strict_collections = config_data.get(const.CONFIG_KEY_STRICT_COLLECTIONS, False)
        exception_tag_requires_justification = config_data.get(const.CONFIG_KEY_TAG_REQUIRES_JUSTIFICATION, False)
        max_exception_tags_per_file = config_data.get(const.CONFIG_KEY_MAX_TAGS_PER_FILE)
        r003_mode = config_data.get(const.CONFIG_KEY_R003_MODE, const.DEFAULT_R003_MODE)
        r006_paths = config_data.get(const.CONFIG_KEY_R006_PATHS, const.DEFAULT_R006_PATHS)
        min_dict_keys = config_data.get(const.CONFIG_KEY_MIN_DICT_KEYS, const.DEFAULT_MIN_DICT_KEYS)
        r003_strict_repr = config_data.get(const.CONFIG_KEY_R003_STRICT_REPR, True)
        r003_sensitivity_bases = config_data.get(const.CONFIG_KEY_R003_SENSITIVITY_BASES, const.DEFAULT_R003_SENSITIVITY_BASES.copy())
        r003_sensitivity_allowlist = config_data.get(const.CONFIG_KEY_R003_SENSITIVITY_ALLOWLIST, [])
        return cls(
            service_paths=service_paths,
            dto_paths=dto_paths,
            exception_tags=exception_tags,
            disabled_rules=disabled_rules,
            severity_overrides=severity_overrides,
            strict_collections=strict_collections,
            exception_tag_requires_justification=exception_tag_requires_justification,
            max_exception_tags_per_file=max_exception_tags_per_file,
            r003_mode=r003_mode,
            r006_paths=r006_paths,
            min_dict_keys=min_dict_keys,
            r003_strict_repr=r003_strict_repr,
            r003_sensitivity_bases=r003_sensitivity_bases,
            r003_sensitivity_allowlist=r003_sensitivity_allowlist,
            loc_cap=loc_cap,
        )

    def is_rule_enabled(self, rule_id: str) -> bool:
        """Check if a rule is enabled."""
        return rule_id not in self.disabled_rules
