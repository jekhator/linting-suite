"""LOC cap enforcer for Python codebases with ratchet baseline semantics."""

import os
from pathlib import Path

import linting_suite.config.constants as const
from linting_suite.inspection import PathClassifier


class LocCap:
    """LOC cap enforcer with configurable hard/soft limits and baseline ratchet."""

    @staticmethod
    def count_lines(file_path: str) -> int:
        """Count all lines (matches wc -l semantics for baseline compatibility)."""
        try:
            with open(file_path, const.FILE_MODE_READ, encoding=const.ENCODING_UTF8) as handle:
                return sum(1 for _ in handle)
        except (OSError, UnicodeDecodeError):
            return 0

    @staticmethod
    def load_baseline(baseline_file: str) -> dict[str, int]:
        """Load baseline LOC counts from file (with fallback for backward compatibility)."""
        baseline: dict[str, int] = {}

        actual_file = None
        if os.path.isfile(baseline_file):
            actual_file = baseline_file
        elif baseline_file == const.DEFAULT_LOC_CAP_BASELINE_FILE:
            for fallback in const.LOC_CAP_BASELINE_LEGACY_NAMES:
                if os.path.isfile(fallback):
                    actual_file = fallback
                    break

        if not actual_file:
            return baseline

        try:
            with open(actual_file, const.FILE_MODE_READ, encoding=const.ENCODING_UTF8) as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.rsplit(const.LOC_BASELINE_SEPARATOR, 1)
                    if len(parts) == const.LOC_BASELINE_PARTS:
                        path, loc_text = parts
                        try:
                            baseline[path.strip()] = int(loc_text.strip())
                        except ValueError:
                            continue
        except OSError:
            pass

        return baseline

    @staticmethod
    def find_python_files(
        root_path: str, exclude_patterns: tuple[str, ...] = const.DEFAULT_EXCLUDE_PATTERNS
    ) -> dict[str, int]:
        """Find all Python files under root_path, exempting test files and excluded patterns."""
        current_locs: dict[str, int] = {}
        root = Path(root_path).resolve()

        if not root.exists():
            return current_locs

        for file_path in root.rglob(const.TEMPLATE_EXTENSION_GLOB.format(extension=const.PY_EXTENSION)):
            file_str = str(file_path)
            if any(excluded in file_str for excluded in exclude_patterns):
                continue

            if PathClassifier.is_loc_test_file(file_path):
                continue

            loc = LocCap.count_lines(file_str)
            current_locs[file_str] = loc

        return current_locs

    @staticmethod
    def generate_baseline(
        root_path: str, exclude_patterns: tuple[str, ...] = const.DEFAULT_EXCLUDE_PATTERNS, floor: int = 0
    ) -> str:
        """Generate baseline output in path:loc format, sorted by LOC descending."""
        files = LocCap.find_python_files(root_path, exclude_patterns)

        filtered = [(path, loc) for path, loc in files.items() if loc >= floor]
        sorted_files = sorted(filtered, key=lambda entry: (-entry[1], entry[0]))

        lines = [const.TEMPLATE_LOC_BASELINE_LINE.format(path=path, loc=loc) for path, loc in sorted_files]
        return const.LINE_SEPARATOR.join(lines)

    @staticmethod
    def run_loc_cap(
        path: str, hard_cap: int = const.DEFAULT_LOC_HARD_CAP,
        soft_target: int = const.DEFAULT_LOC_SOFT_TARGET, baseline_file: str = const.DEFAULT_LOC_CAP_BASELINE_FILE,
        exclude_patterns: tuple[str, ...] = const.DEFAULT_EXCLUDE_PATTERNS, generate: bool = False
    ) -> int:
        """Run LOC cap checker with hard/soft caps and baseline ratchet enforcement."""
        if generate:
            baseline_output = LocCap.generate_baseline(path, exclude_patterns, floor=0)
            print(baseline_output)
            return const.EXIT_CODE_SUCCESS

        baseline = LocCap.load_baseline(baseline_file)
        current = LocCap.find_python_files(path, exclude_patterns)

        soft_warnings = []
        hard_violations = []
        improvements = []

        for path_str, loc in current.items():
            if soft_target < loc <= hard_cap:
                soft_warnings.append(const.MSG_LOC_SOFT_ENTRY.format(loc=loc, path=path_str))

            if loc > hard_cap:
                if path_str not in baseline:
                    hard_violations.append(const.MSG_LOC_NEW_OFFENDER.format(loc=loc, path=path_str))
                elif loc > baseline[path_str]:
                    delta = loc - baseline[path_str]
                    hard_violations.append(
                        const.MSG_LOC_GREW.format(loc=loc, path=path_str, baseline=baseline[path_str], delta=delta)
                    )

        for baseline_path, baseline_loc in baseline.items():
            current_loc = current.get(baseline_path)

            if current_loc is None:
                improvements.append(const.MSG_LOC_DELETED.format(path=baseline_path))
            elif current_loc < baseline_loc:
                if current_loc <= hard_cap:
                    delta = baseline_loc - current_loc
                    improvements.append(
                        const.MSG_LOC_IMPROVED.format(
                            loc=current_loc, path=baseline_path, baseline=baseline_loc, delta=delta
                        )
                    )

        if soft_warnings:
            print(const.MSG_LOC_SOFT_HEADER.format(soft_target=soft_target))
            print(const.LINE_SEPARATOR.join(soft_warnings))
            print()

        if improvements:
            print(const.MSG_LOC_IMPROVED_HEADER.format(hard_cap=hard_cap))
            print(const.LINE_SEPARATOR.join(improvements))
            print()

        if hard_violations:
            print(const.MSG_LOC_HARD_HEADER.format(hard_cap=hard_cap))
            print(const.LINE_SEPARATOR.join(hard_violations))
            print()
            print(const.MSG_LOC_RATIONALE)
            print(const.MSG_LOC_TESTS)
            print(const.MSG_LOC_REFACTOR)
            return const.EXIT_CODE_HIGH_VIOLATION

        print(const.MSG_LOC_WITHIN_CAP.format(hard_cap=hard_cap))
        return const.EXIT_CODE_SUCCESS
