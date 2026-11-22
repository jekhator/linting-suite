"""Checker for R001: Dict[str, Any] or bare collections in signatures."""

import ast

import linting_suite.config.constants as const
from linting_suite.checkers.base import BaseChecker
from linting_suite.inspection import AnnotationInspector, PathClassifier
from linting_suite.rules import RuleSeverity, Violation


class R001Checker(BaseChecker):
    """Check for Dict[str, Any] or bare collections in service-layer function signatures."""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions."""
        if not PathClassifier.is_service_path(
            self.file_path, self.config.service_paths
        ):
            return

        if self.is_suppressed(node, const.RULE_ID_R001):
            return

        for argument in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
            if argument.annotation:
                if AnnotationInspector.is_dict_str_any(argument.annotation):
                    self.violations.append(
                        Violation(
                            rule_id=const.RULE_ID_R001,
                            severity=RuleSeverity.HIGH,
                            file=str(self.file_path),
                            line=node.lineno,
                            col=node.col_offset,
                            message=const.MSG_R001_DICT_STR_ANY.format(name=node.name),
                        )
                    )
                    return
                elif (
                    self.config.strict_collections
                    and AnnotationInspector.is_bare_collection(argument.annotation)
                ):
                    self.violations.append(
                        Violation(
                            rule_id=const.RULE_ID_R001,
                            severity=RuleSeverity.HIGH,
                            file=str(self.file_path),
                            line=node.lineno,
                            col=node.col_offset,
                            message=const.MSG_R001_BARE_COLLECTION.format(name=node.name),
                        )
                    )
                    return

        if node.args.vararg and node.args.vararg.annotation:
            if AnnotationInspector.is_dict_str_any(node.args.vararg.annotation):
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001,
                        severity=RuleSeverity.HIGH,
                        file=str(self.file_path),
                        line=node.lineno,
                        col=node.col_offset,
                        message=const.MSG_R001_DICT_STR_ANY.format(name=node.name),
                    )
                )
                return
            elif (
                self.config.strict_collections
                and AnnotationInspector.is_bare_collection(node.args.vararg.annotation)
            ):
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001,
                        severity=RuleSeverity.HIGH,
                        file=str(self.file_path),
                        line=node.lineno,
                        col=node.col_offset,
                        message=const.MSG_R001_BARE_COLLECTION.format(name=node.name),
                    )
                )
                return

        if node.args.kwarg and node.args.kwarg.annotation:
            if AnnotationInspector.is_dict_str_any(node.args.kwarg.annotation):
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001,
                        severity=RuleSeverity.HIGH,
                        file=str(self.file_path),
                        line=node.lineno,
                        col=node.col_offset,
                        message=const.MSG_R001_DICT_STR_ANY.format(name=node.name),
                    )
                )
                return
            elif (
                self.config.strict_collections
                and AnnotationInspector.is_bare_collection(node.args.kwarg.annotation)
            ):
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001,
                        severity=RuleSeverity.HIGH,
                        file=str(self.file_path),
                        line=node.lineno,
                        col=node.col_offset,
                        message=const.MSG_R001_BARE_COLLECTION.format(name=node.name),
                    )
                )
                return

        if node.returns:
            if AnnotationInspector.is_dict_str_any(node.returns):
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001,
                        severity=RuleSeverity.HIGH,
                        file=str(self.file_path),
                        line=node.lineno,
                        col=node.col_offset,
                        message=const.MSG_R001_DICT_STR_ANY.format(name=node.name),
                    )
                )
            elif (
                self.config.strict_collections
                and AnnotationInspector.is_bare_collection(node.returns)
            ):
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001,
                        severity=RuleSeverity.HIGH,
                        file=str(self.file_path),
                        line=node.lineno,
                        col=node.col_offset,
                        message=const.MSG_R001_BARE_COLLECTION.format(name=node.name),
                    )
                )

        self.generic_visit(node)
