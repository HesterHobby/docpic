import os
import sys

import pytest
from unittest.mock import patch
from pytest_mock import MockFixture

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedTagNameException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from docpic_py.selenium_processor import get_element_from_varname, docpic, select, identify


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
    with pytest.raises(Exception) as exc_info:
        docpic(driver_mock, str(outfile))

    assert "Something went wrong with saving screenshot to" in str(exc_info.value)


def test_select_with_dropdown_element(mocker: MockFixture):
    # Arrange
    element = mocker.Mock(spec=WebElement)
    element.tag_name = 'select'
    labeltext = 'Option 1'
    select_mock = mocker.Mock(spec=Select)
    select_mock.select_by_visible_text.return_value = None
    mocker.patch('docpic_py.selenium_processor.Select', return_value=select_mock)

    # Act
    select(element, labeltext)

    # Assert
    select_mock.select_by_visible_text.assert_called_once_with(labeltext)


def test_select_with_non_dropdown_element(mocker):
    # Arrange
    element = mocker.Mock(spec=WebElement)
    element.tag_name = 'input'
    labeltext = 'Option 1'

    # Act/Assert
    with pytest.raises(UnexpectedTagNameException) as exc_info:
        select(element, labeltext)
        # Assert exception message or any other details, if necessary
        assert str(exc_info.value) == f"\nThe element {element.tag_name} is not a dropdown or has not been clicked"


@pytest.mark.parametrize('varname', [None, 'element1'])
def test_identify_finds_element(mocker, varname):
    # Arrange
    wait_mock = mocker.Mock(spec=WebDriverWait)
    element_mock = mocker.Mock(spec=WebElement)
    selector = 'myElement'

    wait_mock.until.return_value = element_mock

    # Act
    module_vars = {}

    with patch("docpic_py.selenium_processor.module_vars", module_vars):
        result = identify(wait_mock, 'id', selector, varname)

        # Assert
        assert result == element_mock

        if varname is not None:
            assert module_vars[varname] == element_mock


@pytest.mark.parametrize('varname', [None, 'element1'])
def test_identify__does_not_find_element(mocker, varname):
    # Arrange
    wait_mock = mocker.Mock(spec=WebDriverWait)
    selector = 'myElement'

    # Mock the behavior when NoSuchElementException is raised
    wait_mock.until.side_effect = NoSuchElementException()

    # Act
    module_vars = {}

    with patch("docpic_py.selenium_processor.module_vars", module_vars):
        # Assert
        with pytest.raises(NoSuchElementException):
            identify(wait_mock, 'id', selector, varname)

        # Verify that module_vars is not modified when identification fails
        assert varname not in module_vars
