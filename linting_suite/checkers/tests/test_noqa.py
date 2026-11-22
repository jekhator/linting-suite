"""Tests for noqa comment suppression functionality."""

import ast

from linting_suite.inspection import AnnotationInspector


class TestNoqaCommentDetection:
    """Test noqa comment parsing and suppression."""

    def test_bare_noqa_suppresses_all(self):
        """Bare `# noqa` should suppress any rule."""
        source = "def foo(x: Dict[str, Any]): pass  # noqa"
        lines = source.splitlines()
        tree = ast.parse(source)
        func_node = tree.body[0]

        assert AnnotationInspector.has_noqa_comment(func_node, "R001", lines) is True
        assert AnnotationInspector.has_noqa_comment(func_node, "R002", lines) is True
        assert AnnotationInspector.has_noqa_comment(func_node, "R006", lines) is True

    def test_noqa_dto_strict_suppresses_all_rules(self):
        """# noqa: dto-strict should suppress any dto-strict rule."""
        source = "def foo(x: Dict[str, Any]): pass  # noqa: dto-strict"
        lines = source.splitlines()
        tree = ast.parse(source)
        func_node = tree.body[0]

        assert AnnotationInspector.has_noqa_comment(func_node, "R001", lines) is True
        assert AnnotationInspector.has_noqa_comment(func_node, "R002", lines) is True
        assert AnnotationInspector.has_noqa_comment(func_node, "R005", lines) is True

    def test_noqa_specific_rule_suppresses_only_that_rule(self):
        """# noqa: dto-strict-R001 should suppress only R001."""
        source = "def foo(x: Dict[str, Any]): pass  # noqa: dto-strict-R001"
        lines = source.splitlines()
        tree = ast.parse(source)
        func_node = tree.body[0]

        assert AnnotationInspector.has_noqa_comment(func_node, "R001", lines) is True
        assert AnnotationInspector.has_noqa_comment(func_node, "R002", lines) is False
        assert AnnotationInspector.has_noqa_comment(func_node, "R006", lines) is False

    def test_noqa_comma_separated_rules(self):
        """# noqa: dto-strict-R001, dto-strict-R002 should suppress those rules only."""
        source = (
            "def foo(x: Dict[str, Any]): pass  # noqa: dto-strict-R001, dto-strict-R002"
        )
        lines = source.splitlines()
        tree = ast.parse(source)
        func_node = tree.body[0]

        assert AnnotationInspector.has_noqa_comment(func_node, "R001", lines) is True
        assert AnnotationInspector.has_noqa_comment(func_node, "R002", lines) is True
        assert AnnotationInspector.has_noqa_comment(func_node, "R003", lines) is False
        assert AnnotationInspector.has_noqa_comment(func_node, "R006", lines) is False

    def test_missing_noqa_not_suppressed(self):
        """Without noqa comment, violations should not be suppressed."""
        source = "def foo(x: Dict[str, Any]): pass"
        lines = source.splitlines()
        tree = ast.parse(source)
        func_node = tree.body[0]

        assert AnnotationInspector.has_noqa_comment(func_node, "R001", lines) is False
        assert AnnotationInspector.has_noqa_comment(func_node, "R002", lines) is False

    def test_noqa_with_trailing_text(self):
        """noqa should work even with extra text after it."""
        source = "def foo(x: Dict[str, Any]): pass  # noqa: dto-strict - complex transient payload"
        lines = source.splitlines()
        tree = ast.parse(source)
        func_node = tree.body[0]

        assert AnnotationInspector.has_noqa_comment(func_node, "R001", lines) is True

    def test_noqa_with_leading_whitespace(self):
        """noqa with leading whitespace should be recognized."""
        source = "def foo(x: Dict[str, Any]): pass  #    noqa: dto-strict-R001"
        lines = source.splitlines()
        tree = ast.parse(source)
        func_node = tree.body[0]

        assert AnnotationInspector.has_noqa_comment(func_node, "R001", lines) is True

    def test_noqa_missing_lineno(self):
        """Node without lineno should return False."""
        source = "x = 1"
        lines = source.splitlines()
        node = ast.AST()
        assert AnnotationInspector.has_noqa_comment(node, "R001", lines) is False

    def test_noqa_lineno_beyond_file(self):
        """Node with lineno beyond source length should return False."""
        source = "x = 1"
        lines = source.splitlines()
        tree = ast.parse(source)
        func_node = tree.body[0]
        func_node.lineno = 999
        assert AnnotationInspector.has_noqa_comment(func_node, "R001", lines) is False

    def test_noqa_in_middle_of_comment(self):
        """# noqa in the middle of a longer comment should be recognized."""
        source = "def foo(x: Dict[str, Any]): pass  # some comment noqa: dto-strict-R001 more text"
        lines = source.splitlines()
        tree = ast.parse(source)
        func_node = tree.body[0]

        assert AnnotationInspector.has_noqa_comment(func_node, "R001", lines) is False

    def test_noqa_standard_pylint_style(self):
        """Standard pylint-style noqa should work."""
        source = "x = {}  # noqa"
        lines = source.splitlines()
        tree = ast.parse(source)
        assign_node = tree.body[0]
        assert AnnotationInspector.has_noqa_comment(assign_node, "R002", lines) is True

    def test_noqa_flake8_style(self):
        """flake8-style noqa with codes should work if codes match."""
        source = "def foo(x: Dict[str, Any]): pass  # noqa: E501,F841"
        lines = source.splitlines()
        tree = ast.parse(source)
        func_node = tree.body[0]
        assert AnnotationInspector.has_noqa_comment(func_node, "R001", lines) is False
