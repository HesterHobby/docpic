from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import pytest

from docpic_py.webdriver_initializer import initialize_driver


@pytest.mark.slow
def test_initialize_driver_headless_enabled():
    webdriver_options = {'headless': True}
    driver = initialize_driver(webdriver_options)
    assert isinstance(driver, webdriver.Chrome)
    assert '--headless' in driver.options.arguments
    driver.quit()


@pytest.mark.slow
def test_initialize_driver_headless_disabled():
    webdriver_options = {'headless': False}
    driver = initialize_driver(webdriver_options)
    assert isinstance(driver, webdriver.Chrome)
    assert '--headless' not in driver.options.arguments
    driver.quit()


@pytest.mark.slow
def test_initialize_driver_with_additional_options():
    webdriver_options = {'headless': True, 'window-size': '1200x800'}
    driver = initialize_driver(webdriver_options)
    assert isinstance(driver, webdriver.Chrome)
    assert '--headless' in driver.options.arguments
    assert '--window-size=1200x800' in driver.options.arguments
    driver.quit()


@pytest.mark.slow
def test_initialize_driver_with_invalid_options():
    webdriver_options = {'headless': True, 'invalid-option': 'value'}
    driver = initialize_driver(webdriver_options)
    assert isinstance(driver, webdriver.Chrome)
    assert '--headless' in driver.options.arguments
    driver.quit()


def test_initialize_driver_with_webdriver_exception(mocker):
    webdriver_options = {'headless': True}
    mocker.patch.object(ChromeDriverManager, 'install', side_effect=WebDriverException)
    driver = initialize_driver(webdriver_options)
    assert driver is None
