"""Annotation and noqa comment inspection utilities."""

import ast
from typing import Optional

import linting_suite.config.constants as const


class AnnotationInspector:
    """Inspect Python annotations and noqa comments."""

    @staticmethod
    def get_annotation_string(annotation: Optional[ast.expr]) -> str:
        """
        Convert annotation AST node to string representation.

        Handles Python 3.8 compatibility where ast.Index wraps the actual index
        in subscript nodes.
        """
        if annotation is None:
            return ""

        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Subscript):
            base = AnnotationInspector.get_annotation_string(annotation.value)
            if hasattr(ast, const.AST_INDEX_NODE) and isinstance(annotation.slice, ast.Index):
                slice_value = annotation.slice.value  # type: ignore[attr-defined]
                index = AnnotationInspector.get_annotation_string(slice_value)
            else:
                index = AnnotationInspector.get_annotation_string(annotation.slice)
            return const.TEMPLATE_SUBSCRIPT.format(base=base, index=index)
        elif isinstance(annotation, ast.Tuple):
            elements = const.ELEMENT_SEPARATOR.join(
                AnnotationInspector.get_annotation_string(element) for element in annotation.elts
            )
            return const.TEMPLATE_TUPLE.format(elements=elements)
        elif isinstance(annotation, ast.Attribute):
            value = AnnotationInspector.get_annotation_string(annotation.value)
            return const.TEMPLATE_ATTRIBUTE.format(value=value, attribute=annotation.attr)
        elif isinstance(annotation, ast.Constant):
            return repr(annotation.value)
        else:
            return ""

    @staticmethod
    def is_dict_str_any(annotation: Optional[ast.expr]) -> bool:
        """Check if annotation is Dict[str, Any] or dict[str, Any]."""
        if annotation is None:
            return False

        try:
            annotation_text = ast.unparse(annotation)
        except Exception:
            return False

        annotation_lower = annotation_text.lower().replace(const.SPACE, "")
        return const.DICT_STR_ANY_PATTERN in annotation_lower

    @staticmethod
    def is_bare_collection(annotation: Optional[ast.expr]) -> bool:
        """Check if annotation is bare dict, list, or tuple without type parameters."""
        if annotation is None:
            return False

        if isinstance(annotation, ast.Name):
            return annotation.id in const.BARE_COLLECTION_TYPES

        return False

    @staticmethod
    def contains_any(annotation: Optional[ast.expr]) -> bool:
        """Check if annotation contains typing.Any."""
        if annotation is None:
            return False

        try:
            annotation_text = ast.unparse(annotation)
        except Exception:
            return False

        annotation_lower = annotation_text.lower().replace(const.SPACE, "")
        return const.ANY_PATTERN in annotation_lower

    @staticmethod
    def has_noqa_comment(node: ast.AST, rule_id: str, source_lines: list[str]) -> bool:
        """
        Check if node's line has a noqa comment suppressing the given rule.

        Supports backward-compat dto-strict tags and bare rule codes.
        """
        if not hasattr(node, const.ATTRIBUTE_LINENO) or node.lineno is None:
            return False
        if node.lineno > len(source_lines):
            return False

        line = source_lines[node.lineno - 1]

        if const.COMMENT_MARKER not in line:
            return False

        comment_index = line.find(const.COMMENT_MARKER)
        comment_part = line[comment_index + 1 :].strip()

        if not comment_part.startswith(const.NOQA_KEYWORD):
            return False

        noqa_part = comment_part[len(const.NOQA_KEYWORD) :].strip()

        if not noqa_part or noqa_part.startswith(const.COMMENT_MARKER) or noqa_part.startswith(const.NOQA_REASON_DASH):
            return True

        if noqa_part.startswith(const.NOQA_SPEC_SEPARATOR):
            specification = noqa_part[1:].strip()
            if const.COMMENT_MARKER in specification:
                specification = specification.split(const.COMMENT_MARKER)[0].strip()

            parts = specification.split()
            if len(parts) > 1:
                second = parts[1]
                if second and second[0] in const.NOQA_REASON_DASHES:
                    specification = parts[0]

            if specification == const.PREFIX_STRICT_MODULE:
                return True

            if specification == const.TEMPLATE_PREFIXED_RULE.format(prefix=const.PREFIX_STRICT_MODULE, rule_id=rule_id):
                return True

            if specification == const.PREFIX_DTO_STRICT:
                return True

            if specification == const.TEMPLATE_PREFIXED_RULE.format(prefix=const.PREFIX_DTO_STRICT, rule_id=rule_id):
                return True

            tokens = [token.strip() for token in specification.split(const.NOQA_TOKEN_SEPARATOR)]
            if (
                const.TEMPLATE_PREFIXED_RULE.format(prefix=const.PREFIX_STRICT_MODULE, rule_id=rule_id) in tokens
                or const.TEMPLATE_PREFIXED_RULE.format(prefix=const.PREFIX_DTO_STRICT, rule_id=rule_id) in tokens
            ):
                return True

            if rule_id in tokens:
                return True

        return False
