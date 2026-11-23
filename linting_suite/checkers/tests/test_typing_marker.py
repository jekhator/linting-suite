"""Tests that the import root carries the typing marker the classifiers promise."""

import tomllib
from pathlib import Path

import linting_suite


class TestTypingMarker:
    """The Typing :: Typed classifier is backed by a root py.typed file."""

    def test_root_py_typed_exists(self):
        """A py.typed at the import root covers every subpackage."""
        root = Path(linting_suite.__file__).parent

        assert (root / "py.typed").is_file()

    def test_classifier_and_marker_agree(self):
        """If the project claims to be typed, the marker must ship with it."""
        root = Path(linting_suite.__file__).parent
        pyproject = root.parent / "pyproject.toml"
        classifiers = tomllib.loads(pyproject.read_text())["project"]["classifiers"]

        assert "Typing :: Typed" in classifiers
        assert (root / "py.typed").is_file()
