"""Tests for loc-cap test file exemption."""

from linting_suite.loc_cap import LocCap


class TestLocCapTestExemption:
    """Test suite for related functionality."""

    def test_loc_cap_exempts_test_basename(self, temp_project_with_test_files):
        """Test files matching test_*.py are exempt."""
        files = LocCap.find_python_files(str(temp_project_with_test_files))
        for path, loc in files.items():
            assert "test_module.py" not in path, "test_*.py files should be exempt"

    def test_loc_cap_exempts_conftest(self, temp_project_with_test_files):
        """conftest.py files are exempt."""
        files = LocCap.find_python_files(str(temp_project_with_test_files))
        for path in files.keys():
            assert "conftest.py" not in path, "conftest.py should be exempt"

    def test_loc_cap_exempts_tests_directory(self, temp_project_with_test_files):
        """Files under tests/ directory are exempt."""
        files = LocCap.find_python_files(str(temp_project_with_test_files))
        for path in files.keys():
            assert "/tests/" not in path and not path.startswith("tests/"), "Files under tests/ should be exempt"

    def test_loc_cap_counts_source_files(self, temp_project_with_test_files):
        """Source files that are not test files are counted."""
        files = LocCap.find_python_files(str(temp_project_with_test_files))
        found_source = False
        for path, loc in files.items():
            if "src/module.py" in path or "src" + chr(92) + "module.py" in path:
                found_source = True
                assert loc == 500, "Source file should be counted with correct line count"
        assert found_source, "Source file should be present in results"
