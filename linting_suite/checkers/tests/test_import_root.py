"""Tests that every subpackage lives under the linting_suite import root."""

import importlib

import pytest

SUBPACKAGES = ("checkers", "config", "inspection", "linter", "loc_cap", "rules", "module")
OLD_PREFIX = "strict" + "_"
OLD_ROOTS = tuple(OLD_PREFIX + name for name in SUBPACKAGES)


class TestImportRoot:
    """Import root layout after the rename."""

    @pytest.mark.parametrize("name", SUBPACKAGES)
    def test_new_subpackage_imports(self, name):
        """Each subpackage imports under linting_suite."""
        assert importlib.import_module(f"linting_suite.{name}")

    @pytest.mark.parametrize("name", OLD_ROOTS)
    def test_old_root_does_not_import(self, name):
        """Old top-level names no longer resolve."""
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(name)
