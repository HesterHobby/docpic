from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest

from python.webdriver_initializer import initialize_driver


def test_initialize_driver_headless_enabled():
    webdriver_options = {'headless': True}
    driver = initialize_driver(webdriver_options)
    assert isinstance(driver, webdriver.Chrome)
    assert driver.options.headless
    driver.quit()


def test_initialize_driver_headless_disabled():
    webdriver_options = {'headless': False}
    driver = initialize_driver(webdriver_options)
    assert isinstance(driver, webdriver.Chrome)
    assert not driver.options.headless
    driver.quit()


def test_initialize_driver_with_additional_options():
    webdriver_options = {'headless': True, 'window-size': '1200x800'}
    driver = initialize_driver(webdriver_options)
    assert isinstance(driver, webdriver.Chrome)
    assert driver.options.headless
    assert '--window-size=1200x800' in driver.options.arguments
    driver.quit()


def test_initialize_driver_with_invalid_options():
    webdriver_options = {'headless': True, 'invalid-option': 'value'}
    driver = initialize_driver(webdriver_options)
    assert isinstance(driver, webdriver.Chrome)
    assert driver.options.headless
    driver.quit()

def test_initialize_driver_with_webdriver_exception(mocker):
    webdriver_options = {'headless': True}
    mocker.patch.object(ChromeDriverManager, 'install', side_effect=WebDriverException)
    driver = initialize_driver(webdriver_options)
    assert driver is None