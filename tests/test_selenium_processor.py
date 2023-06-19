import os
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from docpic_py.selenium_processor import get_element_from_varname, docpic
from unittest.mock import patch

# Add the project root directory to the Python module search path
current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)


def test_get_element_from_varname_existing_element():
    # Arrange
    varname = "element1"
    element1 = WebElement(parent='dummy_parent', id_='dummy_id')  # Create a dummy WebElement for testing
    module_vars = {"element1": element1}

    with patch("docpic_py.selenium_processor.module_vars", module_vars):
        # Act
        result = get_element_from_varname(varname)

        # Assert
        assert result == element1


def test_get_element_from_varname_nonexistent_element():
    # Arrange
    varname = "element2"
    module_vars = {}

    with patch("docpic_py.selenium_processor.module_vars", module_vars):
        # Act and Assert
        with pytest.raises(KeyError):
            get_element_from_varname(varname)


@pytest.mark.slow
def test_docpic_saves_screenshot(tmp_path):
    # Arrange
    outfile = tmp_path / "screenshot.png"
    driver_mock = webdriver.Chrome()

    # Act
    docpic(driver_mock, str(outfile))

    # Assert
    assert outfile.exists()


@pytest.mark.slow
def test_docpic_handles_exception(tmp_path, capsys):
    # Arrange
    outfile = tmp_path / "screenshot.png"
    driver_mock = webdriver.Chrome()

    # Patch the save_screenshot method to raise an exception
    with patch.object(driver_mock, 'save_screenshot', side_effect=Exception):
        # Act
        with pytest.raises(Exception):
            docpic(driver_mock, str(outfile))

        # Assert
        captured = capsys.readouterr()
        assert f"Error saving output file to {outfile}" in captured.out


@pytest.mark.slow
def test_docpic_raises_exception_if_file_not_created(tmp_path):
    # Arrange
    outfile = tmp_path / "non_existent_folder/screenshot.png"
    driver_mock = webdriver.Chrome()

    # Act and Assert
    with pytest.raises(Exception) as excinfo:
        docpic(driver_mock, str(outfile))

    assert "Something went wrong with saving screenshot to" in str(excinfo.value)
