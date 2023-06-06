from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, UnexpectedTagNameException

import yaml

from yaml_validator import validate_yaml_schema
from webdriver_initializer import initialize_driver

module_vars = {}


def take_screenshot_from_yaml(config_file):
    # Load the YAML configuration file
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    except Exception:
        print("Could not open config file " + config_file)
        raise

    # Validate the YAML schema
    if not validate_yaml_schema(config):
        print("Invalid YAML schema.")
        return

    # Extract the configuration values
    url = config['url']
    steps = config['steps']

    # Get options from the YAML data, if available
    options = config.get('webdriver_options', None)

    # Launch ChromeDriver with the specified path and options
    driver = initialize_driver(options)

    if driver is None:
        print("Driver initialisation failed")
        return

    # Visit the specified URL
    driver.get(url)

    # Send it off to recursive function to deal with steps.
    for step in steps:
        execute_step(step, driver)

    driver.quit()


# Function that deals with steps
def execute_step(step, driver: webdriver):  # Not sure what type steps is here

    # Create WebDriverWait object outside the loop
    wait = WebDriverWait(driver, 10)
    type = step.get("type")

    if type == "identify":
        element = identify(wait, step.get("using"), step.get("selector"), step.get("var"))
        return element

    if type == "var-ref":
        element = get_element_from_varname(step.get("var-name"))
        return element

    if type == "click":
        element = execute_step(step.get("target"), driver) if step.get("target") else None
        click(element)

    if type == "enter-text":
        element = execute_step(step.get("target"), driver) if step.get("target") else None
        enter_text(element, step.get("value"))

    if type == "select":
        element = execute_step(step.get("target"), driver) if step.get("target") else None
        select(element, step.get("value"))

    if type == "docpic":
        outfile = step.get("outfile")
        docpic(driver, outfile)


def identify(wait: WebDriverWait, using: str, selector: str, varname: str):
    by_mapping = {
        'id': By.ID,
        'class': By.CLASS_NAME,
        'tag': By.TAG_NAME,
        'name': By.NAME,
        'link': By.LINK_TEXT,
        'partial_link': By.PARTIAL_LINK_TEXT,
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH
    }

    locator_type = by_mapping.get(using)

    # Get the item, add to varname
    try:
        element = wait.until(EC.visibility_of_element_located((locator_type, selector)))
    except NoSuchElementException:
        print("The element" + selector + " was not found on this page")
        raise

    if varname is not None:
        module_vars[varname] = element
    return element


def click(element: WebElement):
    element.click()


def enter_text(element: WebElement, text: str):
    element.send_keys(text)


def select(element: WebElement, labeltext: str):
    # Is the element a dropdown?
    try:
        dropdown = Select(element)
    except UnexpectedTagNameException:
        print("The element " + element.tag_name + " is not a dropdown or has not been clicked")
        raise

    dropdown.select_by_visible_text(labeltext)


def docpic(driver: webdriver, outfile: str):
    try:
        driver.save_screenshot(outfile)
        print("Screenshot has been saved to " + outfile)
    except Exception:
        print("Error saving output file to " + outfile)
        raise


def get_element_from_varname(varname: str) -> WebElement:
    element = module_vars.get(varname)
    if element is None:
        raise KeyError("The element variable " + varname + " does not exist in the module level variables")
    return element
