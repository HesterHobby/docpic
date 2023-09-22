import os
import sys
from unittest import mock

import pytest
from unittest.mock import patch, Mock
from pytest_mock import MockFixture

from selenium import webdriver
from selenium.common.exceptions import UnexpectedTagNameException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from docpic_py import selenium_processor
from docpic_py.selenium_processor import get_element_from_varname, docpic, select, identify, execute_step, \
    get_environment_variable, take_screenshot_from_yaml_file
from docpic_py.webdriver_initializer import initialize_driver

# Add the project root directory to the Python module search path
current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)


@pytest.mark.slow
def test_screenshot_from_yaml_file_with_initial_condition(tmp_path):
    # Arrange. Note the yaml file also tests the initial condition, and running headless.
    yaml_file = "./inputs/test_config.dp.yaml"
    outfile = tmp_path / "test.png"

    take_screenshot_from_yaml_file(yaml_file, str(tmp_path))

    assert outfile.exists()


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


def test_get_environment_variable_existing_variable():
    # Arrange
    envvarname = 'MY_VARIABLE'
    varname = None
    with patch.dict(os.environ, {envvarname: 'my_value'}):
        # Act
        result = get_environment_variable(envvarname, varname)

        # Assert
        assert result == 'my_value'


def test_get_environment_variable_non_existing_variable():
    # Arrange
    envvarname = 'NON_EXISTING_VARIABLE'
    varname = None
    with patch.dict(os.environ, clear=True):
        # Act
        result = get_environment_variable(envvarname, varname)

        # Assert
        assert result is None


def test_get_environment_variable_store_in_varname():
    # Arrange
    envvarname = 'MY_VARIABLE'
    varname = 'my_var'
    with patch.dict(os.environ, {envvarname: 'my_value'}), patch('docpic_py.selenium_processor.module_vars', {}):
        # Act
        result = get_environment_variable(envvarname, varname)

        # Assert
        assert result == 'my_value'
        assert selenium_processor.module_vars[varname] == 'my_value'


@pytest.mark.slow
def test_docpic_saves_screenshot(tmp_path):
    # Arrange
    outfile = tmp_path / "screenshot.png"
    driver_mock = initialize_driver(None)

    # Act
    docpic(driver_mock, str(outfile))

    # Assert
    assert outfile.exists()


@pytest.mark.slow
def test_docpic_handles_exception(tmp_path, capsys):
    # Arrange
    outfile = tmp_path / "screenshot.png"
    driver_mock = initialize_driver(None)

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
    driver_mock = initialize_driver(None)

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


def test_select_with_missing_element(mocker):
    # Arrange
    element = mocker.Mock(spec=WebElement)
    element.tag_name = 'select'
    labeltext = 'Option 1'
    select_mock = mocker.Mock(spec=Select)
    select_mock.select_by_visible_text.side_effect = NoSuchElementException("Element not found")
    mocker.patch('docpic_py.selenium_processor.Select', return_value=select_mock)

    # Act/Assert
    with pytest.raises(NoSuchElementException):
        select(element, labeltext)

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
def test_identify_does_not_find_element(mocker, varname):
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


# Below here a bunch of stuff to test the integrated function
# Mocked dependencies and functions
@pytest.fixture
def mock_identify(mocker):
    return mocker.patch("docpic_py.selenium_processor.identify")


@pytest.fixture
def mock_get_element_from_varname(mocker):
    return mocker.patch("docpic_py.selenium_processor.get_element_from_varname")


@pytest.fixture
def mock_click(mocker):
    return mocker.patch("docpic_py.selenium_processor.click")


@pytest.fixture
def mock_clear(mocker):
    return mocker.patch("docpic_py.selenium_processor.clear")


@pytest.fixture
def mock_enter_text(mocker):
    return mocker.patch("docpic_py.selenium_processor.enter_text")


@pytest.fixture
def mock_select(mocker):
    return mocker.patch("docpic_py.selenium_processor.select")


@pytest.fixture
def mock_driver_wait(mocker):
    return mocker.patch("docpic_py.selenium_processor.driver_wait")


@pytest.fixture
def mock_docpic(mocker):
    return mocker.patch("docpic_py.selenium_processor.docpic")


# Mocked webdriver object
@pytest.fixture
def mock_webdriver():
    return Mock()


# Test cases
def test_execute_step_identify(mock_identify, mock_get_element_from_varname):
    # Arrange
    step = {
        "type": "identify",
        "using": "id",
        "selector": "myElement",
        "var": "element1"
    }

    # Act
    execute_step(step, mock_webdriver)

    # Assert
    mock_identify.assert_called_once()
    assert mock_identify.call_args[0] == (mock.ANY, "id", "myElement", "element1")


def test_execute_step_var_ref(mock_identify, mock_get_element_from_varname):
    # Arrange
    step = {
        "type": "var-ref",
        "var-name": "element1"
    }

    # Act
    execute_step(step, mock_webdriver)

    # Assert
    assert not mock_identify.called
    mock_get_element_from_varname.assert_called_once_with("element1")


# Todo: Add a similar test for env-var.


# Test case for step type "click"
def test_execute_step_click(mock_identify, mock_get_element_from_varname, mock_webdriver):
    # Arrange
    step = {
        "type": "click",
        "target": {
            "type": "identify",
            "using": "id",
            "selector": "myElement",
            "var": None
        }
    }

    # Act
    execute_step(step, mock_webdriver)

    # Assert
    mock_identify.assert_called_once_with(mock.ANY, "id", "myElement", None)
    assert not mock_get_element_from_varname.called


# Test case for step type "clear"
def test_execute_step_clear(mock_identify, mock_get_element_from_varname, mock_webdriver):
    # Arrange
    step = {
        "type": "clear",
        "target": {
            "type": "var-ref",
            "var-name": "element1"
        }
    }

    # Act
    execute_step(step, mock_webdriver)

    # Assert
    mock_get_element_from_varname.assert_called_once_with("element1")
    assert not mock_identify.called


# Test case for step type "enter-text"
def test_execute_step_enter_text(mock_identify, mock_get_element_from_varname, mock_webdriver):
    # Arrange
    step = {
        "type": "enter-text",
        "target": {
            "type": "identify",
            "using": "id",
            "selector": "myElement",
            "var": None
        },
        "value": "Hello, World!"
    }

    # Create a mock for the WebElement
    element_mock = Mock()

    # Patch the identify function to return the mock element
    mock_identify.return_value = element_mock

    # Act
    execute_step(step, mock_webdriver)

    # Assert
    mock_identify.assert_called_once_with(mock.ANY, "id", "myElement", None)
    assert not mock_get_element_from_varname.called
    element_mock.send_keys.assert_called_once_with("Hello, World!")

# Todo: Add another test for passing a step as a value.

def test_execute_step_select(mock_identify, mock_get_element_from_varname, mock_webdriver):
    # Arrange
    step = {
        "type": "select",
        "target": {
            "type": "identify",
            "using": "id",
            "selector": "myElement",
            "var": None
        },
        "value": "Option 1"
    }

    # Create a mock for the WebElement representing a dropdown
    element_mock = mock_identify.return_value

    # Mock the required methods for a dropdown element
    element_mock.tag_name = "select"

    # Create a list of mocked option elements
    option_1 = mock.Mock(spec=WebElement)
    option_1.text = "Option 1"
    option_2 = mock.Mock(spec=WebElement)
    option_2.text = "Option 2"
    options = [option_1, option_2]

    # Mock the find_elements method to return the list of options
    element_mock.find_elements.return_value = options

    # Act
    execute_step(step, mock_webdriver)

    # Assert
    mock_identify.assert_called_once_with(mock.ANY, "id", "myElement", None)
    assert not mock_get_element_from_varname.called
    element_mock.find_elements.assert_called_once_with('xpath', './/option[normalize-space(.) = "Option 1"]')


def test_execute_step_wait(mocker):
    # Arrange
    step = {
        "type": "wait",
        "value": 5
    }
    driver_mock = mocker.Mock()
    wait_mock = mocker.patch("docpic_py.selenium_processor.time.sleep")

    # Act
    execute_step(step, driver_mock)

    # Assert
    wait_mock.assert_called_once_with(5)


def test_execute_step_docpic(mocker):
    # Arrange
    step = {
        "type": "docpic",
        "outfile": "screenshot.png"
    }
    driver_mock = mocker.Mock(spec=webdriver.Chrome)
    save_screenshot_mock = mocker.patch.object(driver_mock, "save_screenshot")
    exists_mock = mocker.patch("os.path.exists")

    # Act
    execute_step(step, driver_mock)

    # Assert
    save_screenshot_mock.assert_called_once_with("screenshot.png")
    exists_mock.assert_called_once_with("screenshot.png")

# Add test case for invalid step type

