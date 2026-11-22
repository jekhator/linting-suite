"""Checker for R015: Wrap-path separation (P16 - blank-line rhythm in try/except)."""

import ast

import linting_suite.config.constants as const
from linting_suite.checkers.base import BaseChecker
from linting_suite.rules import RuleSeverity, Violation


class R015Checker(BaseChecker):
    """
    Check wrap-path blank-line rhythm per P16 final calibration.

    Applies ONLY to wrap-function try/except constructs:
    - Nested function inside a wrapper class/method
    - Try/except block with re-raise in except
    - NOT handler if/else constructs

    Checks exactly two things:
    (a) Statement groups within a leg are separated by EXACTLY one blank line
        - Flag 2+ consecutive blanks inside a leg
    (b) The timing-capture pair (perf_counter assignment + round latency line)
        is contiguous - flag any blank inside it
    """

    def visit_Try(self, node: ast.Try) -> None:
        """Visit try statements to check wrap-path blank-line rhythm."""
        if self.is_suppressed(node, const.RULE_ID_R015):
            self.generic_visit(node)
            return

        if node.lineno is None or node.end_lineno is None:
            self.generic_visit(node)
            return

        if self._is_wrap_function_try(node):
            self._check_wrap_function_structure(node)

        self.generic_visit(node)

    def _is_wrap_function_try(self, node: ast.Try) -> bool:
        """Check if try block is within a wrap function (nested inside wrapper class method)."""
        if not node.handlers:
            return False

        for handler in node.handlers:
            for statement in handler.body:
                if isinstance(statement, ast.Raise):
                    return True

        return False

    def _check_wrap_function_structure(self, node: ast.Try) -> None:
        """Check per-leg blank-line structure."""
        if node.body:
            self._check_leg_structure(node.body, node.lineno, const.LEG_TRY)

        for handler in node.handlers:
            if handler.body:
                self._check_leg_structure(handler.body, handler.lineno, const.LEG_EXCEPT)

    def _check_leg_structure(
        self, statements: list[ast.stmt], start_line: int | None, leg_type: str
    ) -> None:
        """Check per-leg structure: group separation and timing-capture contiguity."""
        if not statements or start_line is None:
            return

        self._check_timing_capture_contiguity(statements)

        self._check_group_separation(statements, leg_type)

    def _check_group_separation(
        self, statements: list[ast.stmt], leg_type: str
    ) -> None:
        """
        Check that statement groups are separated by EXACTLY one blank line.

        The gap is the line distance between two statements: 1 is contiguous, 2 is one blank line, more is too many.
        """
        for index in range(len(statements) - 1):
            current = statements[index]
            next_statement = statements[index + 1]

            if current.end_lineno is None or next_statement.lineno is None:
                continue

            gap = next_statement.lineno - current.end_lineno
            if gap > const.R015_MAX_GROUP_GAP:
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R015,
                        severity=RuleSeverity.INFO,
                        file=str(self.file_path),
                        line=next_statement.lineno,
                        col=0,
                        message=const.MSG_R015_GROUPS.format(leg=leg_type.capitalize()),
                    )
                )

    def _check_timing_capture_contiguity(self, statements: list[ast.stmt]) -> None:
        """Check that timing-capture pair (perf_counter + latency calculation) has zero internal blanks."""
        for index in range(len(statements) - 1):
            current = statements[index]
            next_statement = statements[index + 1]

            if self._is_timing_start(current) and self._is_timing_end(next_statement):
                if current.end_lineno is not None and next_statement.lineno is not None:
                    gap = next_statement.lineno - current.end_lineno
                    if gap > 1:
                        self.violations.append(
                            Violation(
                                rule_id=const.RULE_ID_R015,
                                severity=RuleSeverity.INFO,
                                file=str(self.file_path),
                                line=next_statement.lineno,
                                col=0,
                                message=const.MSG_R015_TIMING,
                            )
                        )

    def _is_timing_start(self, statement: ast.stmt) -> bool:
        """Check if statement is a timing-start (perf_counter call)."""
        if not isinstance(statement, ast.Assign):
            return False
        return self._contains_perf_counter(statement.value)

    def _is_timing_end(self, statement: ast.stmt) -> bool:
        """Check if statement is a timing-end (latency calculation)."""
        if not isinstance(statement, ast.Assign):
            return False
        for target in statement.targets:
            if isinstance(target, ast.Name) and const.TIMING_TARGET_MARKER in target.id:
                return self._contains_round(statement.value)
        return False

    def _contains_perf_counter(self, node: ast.expr) -> bool:
        """Check if node contains perf_counter call."""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    if child.func.attr == const.TIMING_CLOCK_NAME:
                        return True
                elif isinstance(child.func, ast.Name):
                    if child.func.id == const.TIMING_CLOCK_NAME:
                        return True
        return False

    def _contains_round(self, node: ast.expr) -> bool:
        """Check if node contains round call."""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    if child.func.id == const.FUNCTION_ROUND:
                        return True
        return False
