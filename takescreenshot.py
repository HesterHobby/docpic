from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

import yaml

from yaml_validator import validate_yaml_schema
from yaml_validator import validate_new_yaml_schema
from webdriver_initializer import initialize_driver

module_vars = {}


def take_screenshot_from_yaml(config_file, output_file):
    # Load the YAML configuration file
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

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

    # Create WebDriverWait object outside the loop
    wait = WebDriverWait(driver, 10)

    # Perform the steps
    for step in steps:
        element_locator = step['element_locator']
        element_locator_value = step['element_locator_value']
        interaction = step['interaction']
        interaction_value = step.get('interaction_value')

        # Find the element based on the locator
        element = wait.until(EC.presence_of_element_located((getattr(By, element_locator), element_locator_value)))
        # Perform the specified interaction with the element
        if interaction == 'click':
            element.click()
        elif interaction == 'write_text':
            element.send_keys(interaction_value)

    # Wait for the final element.
    final_element = config.get('final_element')
    element_locator = final_element['element_locator']
    element_locator_value = final_element['element_locator_value']
    wait.until(EC.presence_of_element_located((getattr(By, element_locator), element_locator_value)))

    # Take a screenshot and save it to the output file
    driver.save_screenshot(output_file)

    # Close the browser
    driver.quit()


def take_screenshot_from_yaml_new(config_file):
    # Load the YAML configuration file
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    except:
        print("Could not open config file " + config_file)
        raise

    # Validate the YAML schema
    if not validate_new_yaml_schema(config):
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


# Function that deals with steps
def execute_step(step, driver: webdriver):  # Not sure what type steps is here
    print("Recursion not working atm, otherwise OK")
    # Create WebDriverWait object outside the loop
    wait = WebDriverWait(driver, 10)
    if step.get("target") is None or step.get("target").get("type") == "var-ref":
        # No targets required or our target is assigned to a variable - we are at the final level.
        # This is clunky and likely to need changing.

        # Do stuff
        type = step.get("type")
        if type == "identify":
            identify(wait, step.get("using"), step.get("selector"), step.get("var"))
            return

        if type == "click":
            target = step.get("target")
            if target.get("type") == "var-ref":
                click(target.get("var-name"))
            else:
                click()  # Using tempvar. I don't believe we currently hit this line ever.
            return

        if type == "enter-text":
            target = step.get("target")
            text = step.get("value")
            if target.get("type") == "var-ref":
                enter_text(text, target.get("var-name"))
            else:
                enter_text(text)  # Using tempvar
            return

        if type == "docpic":
            outputfile = step.get("outfile")
            docpic(driver, outputfile)
            return

    # In case of an undefined target: recur.
    execute_step(step.get("target"), driver)

    # Can we do the calling with tempvar here??
    print("we have reached the end of the recursion")


def identify(wait: WebDriverWait, using: str, selector: str, varname: str):
    if varname is None:
        varname = "tempvar"
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
    element = None
    try:
        element = wait.until(EC.visibility_of_element_located((locator_type, selector)))
    except NoSuchElementException:
        print("The element" + selector + " was not found on this page")
        raise
    module_vars[varname] = element


def click(element_var_name: str = "tempvar"):
    element = get_element_from_varname(element_var_name)
    element.click()


def enter_text(text: str, element_var_name: str = "tempvar"):
    element = get_element_from_varname(element_var_name)
    element.send_keys(text)


def docpic(driver: webdriver, outfile: str):
    try:
        driver.save_screenshot(outfile)
        print("Screenshot has been saved to " + outfile)
    except:
        print("Error saving output file to " + outfile)
        raise


def get_element_from_varname(varname: str) -> WebElement:
    element = module_vars.get(varname)
    if element is None:
        raise KeyError("The element variable " + varname + " does not exist in the module level variables")
    return element
