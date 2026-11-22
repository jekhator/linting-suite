"""Command-line interface for strict-module (formerly dto-strict)."""

import argparse
import json
import sys
from pathlib import Path

import linting_suite.config.constants as const
from linting_suite.config._config import Config
from linting_suite.linter import BaselineLoadError, DtoStrictLinter
from linting_suite.loc_cap import LocCap


def handle_loc_cap(args: list[str]) -> int:
    """Handle loc-cap subcommand (invoked when sys.argv[1] == 'loc-cap')."""
    parser = argparse.ArgumentParser(
        prog=const.CLI_PROG_LOC_CAP,
        description=const.CLI_DESCRIPTION_LOC_CAP,
    )
    parser.add_argument(const.CLI_ARG_PATH, help=const.CLI_HELP_LOC_PATH)
    parser.add_argument(
        const.CLI_FLAG_CONFIG,
        default=const.DEFAULT_CONFIG_FILE,
        help=const.CLI_HELP_CONFIG,
    )
    parser.add_argument(
        const.CLI_FLAG_HARD_CAP,
        type=int,
        help=const.CLI_HELP_HARD_CAP,
    )
    parser.add_argument(
        const.CLI_FLAG_SOFT_TARGET,
        type=int,
        help=const.CLI_HELP_SOFT_TARGET,
    )
    parser.add_argument(
        const.CLI_FLAG_BASELINE,
        help=const.CLI_HELP_LOC_BASELINE,
    )
    parser.add_argument(
        const.CLI_FLAG_GENERATE_BASELINE,
        action=const.CLI_ACTION_STORE_TRUE,
        help=const.CLI_HELP_LOC_GENERATE_BASELINE,
    )

    parsed = parser.parse_args(args[const.CLI_ARGUMENTS_OFFSET:])

    config_path = Path(parsed.config)
    config = Config.from_pyproject(config_path)
    hard_cap = (
        parsed.hard_cap if parsed.hard_cap is not None else config.loc_cap.hard_cap
    )
    soft_target = (
        parsed.soft_target
        if parsed.soft_target is not None
        else config.loc_cap.soft_target
    )
    baseline_file = parsed.baseline if parsed.baseline else config.loc_cap.baseline_file

    return LocCap.run_loc_cap(
        path=parsed.path,
        hard_cap=hard_cap,
        soft_target=soft_target,
        baseline_file=baseline_file,
        generate=parsed.generate_baseline,
    )


def main() -> int:
    """Main CLI entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == const.CLI_SUBCOMMAND_LOC_CAP:
        return handle_loc_cap(sys.argv)

    parser = argparse.ArgumentParser(
        description=const.CLI_DESCRIPTION
    )
    parser.add_argument(const.CLI_ARG_PATH, nargs=const.CLI_NARGS_ANY, help=const.CLI_HELP_PATH)
    parser.add_argument(
        const.CLI_FLAG_CONFIG,
        default=const.DEFAULT_CONFIG_FILE,
        help=const.CLI_HELP_CONFIG,
    )
    parser.add_argument(
        const.CLI_FLAG_FORMAT,
        choices=const.VALID_FORMATS,
        default=const.FORMAT_TEXT,
        help=const.CLI_HELP_FORMAT,
    )
    parser.add_argument(
        const.CLI_FLAG_GENERATE_BASELINE,
        action=const.CLI_ACTION_STORE_TRUE,
        help=const.CLI_HELP_GENERATE_BASELINE,
    )
    parser.add_argument(
        const.CLI_FLAG_BASELINE,
        type=Path,
        help=const.CLI_HELP_BASELINE,
    )

    args = parser.parse_args()

    config_path = Path(args.config)
    config = Config.from_pyproject(config_path)

    if args.generate_baseline:
        if not args.path:
            print(const.ERR_GENERATE_BASELINE_REQUIRES_PATH, file=sys.stderr)
            return const.EXIT_CODE_HIGH_VIOLATION

        all_violations = []
        for path_str in args.path:
            target_path = Path(path_str)
            linter = DtoStrictLinter(config)
            all_violations.extend(linter.lint_path(target_path))

        baseline_data = linter.generate_baseline(all_violations)
        print(json.dumps(baseline_data, indent=const.JSON_INDENT))
        return const.EXIT_CODE_SUCCESS

    if not args.path:
        print(
            const.ERR_PATH_REQUIRED,
            file=sys.stderr,
        )
        return const.EXIT_CODE_HIGH_VIOLATION

    for path_str in args.path:
        target_path = Path(path_str)
        if not target_path.exists():
            print(const.ERR_NONEXISTENT_PATH.format(path=path_str), file=sys.stderr)
            return const.EXIT_CODE_HIGH_VIOLATION

    baseline = None
    if args.baseline:
        try:
            baseline = DtoStrictLinter.load_baseline(args.baseline)
            baseline_count = len(baseline)
            print(
                const.MSG_BASELINE_LOADED.format(count=baseline_count, path=args.baseline),
                file=sys.stderr,
            )
        except BaselineLoadError as error:
            print(str(error), file=sys.stderr)
            return const.EXIT_CODE_HIGH_VIOLATION

    linter = DtoStrictLinter(config, baseline=baseline)
    all_violations = []
    for path_str in args.path:
        target_path = Path(path_str)
        all_violations.extend(linter.lint_path(target_path))

    if all_violations:
        output = linter.format_violations(all_violations, args.format)
        print(output)

    return linter.get_exit_code(all_violations)


if __name__ == "__main__":
    sys.exit(main())
