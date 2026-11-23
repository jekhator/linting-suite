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
        if not PathClassifier.is_service_path(self.file_path, self.config.service_paths):
            return

        if self.is_suppressed(node, const.RULE_ID_R001):
            return

        for argument in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
            if argument.annotation:
                if AnnotationInspector.is_dict_str_any(argument.annotation):
                    file = str(self.file_path)
                    message = const.MSG_R001_DICT_STR_ANY.format(name=node.name)
                    self.violations.append(
                        Violation(
                            rule_id=const.RULE_ID_R001, severity=RuleSeverity.HIGH, file=file,
                            line=node.lineno, col=node.col_offset, message=message
                        )
                    )
                    return
                elif self.config.strict_collections and AnnotationInspector.is_bare_collection(argument.annotation):
                    file = str(self.file_path)
                    message = const.MSG_R001_BARE_COLLECTION.format(name=node.name)
                    self.violations.append(
                        Violation(
                            rule_id=const.RULE_ID_R001, severity=RuleSeverity.HIGH, file=file,
                            line=node.lineno, col=node.col_offset, message=message
                        )
                    )
                    return

        if node.args.vararg and node.args.vararg.annotation:
            if AnnotationInspector.is_dict_str_any(node.args.vararg.annotation):
                file = str(self.file_path)
                message = const.MSG_R001_DICT_STR_ANY.format(name=node.name)
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001, severity=RuleSeverity.HIGH, file=file,
                        line=node.lineno, col=node.col_offset, message=message
                    )
                )
                return
            elif (
                self.config.strict_collections
                and AnnotationInspector.is_bare_collection(node.args.vararg.annotation)
            ):
                file = str(self.file_path)
                message = const.MSG_R001_BARE_COLLECTION.format(name=node.name)
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001, severity=RuleSeverity.HIGH, file=file,
                        line=node.lineno, col=node.col_offset, message=message
                    )
                )
                return

        if node.args.kwarg and node.args.kwarg.annotation:
            if AnnotationInspector.is_dict_str_any(node.args.kwarg.annotation):
                file = str(self.file_path)
                message = const.MSG_R001_DICT_STR_ANY.format(name=node.name)
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001, severity=RuleSeverity.HIGH, file=file,
                        line=node.lineno, col=node.col_offset, message=message
                    )
                )
                return
            elif (
                self.config.strict_collections
                and AnnotationInspector.is_bare_collection(node.args.kwarg.annotation)
            ):
                file = str(self.file_path)
                message = const.MSG_R001_BARE_COLLECTION.format(name=node.name)
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001, severity=RuleSeverity.HIGH, file=file,
                        line=node.lineno, col=node.col_offset, message=message
                    )
                )
                return

        if node.returns:
            if AnnotationInspector.is_dict_str_any(node.returns):
                file = str(self.file_path)
                message = const.MSG_R001_DICT_STR_ANY.format(name=node.name)
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001, severity=RuleSeverity.HIGH, file=file,
                        line=node.lineno, col=node.col_offset, message=message
                    )
                )
            elif self.config.strict_collections and AnnotationInspector.is_bare_collection(node.returns):
                file = str(self.file_path)
                message = const.MSG_R001_BARE_COLLECTION.format(name=node.name)
                self.violations.append(
                    Violation(
                        rule_id=const.RULE_ID_R001, severity=RuleSeverity.HIGH, file=file,
                        line=node.lineno, col=node.col_offset, message=message
                    )
                )

        self.generic_visit(node)
