from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yaml
from selenium import webdriver

from yaml_validator import validate_yaml_schema
from webdriver_initializer import initialize_driver

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

    if driver == None:
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

def take_screenshot_from_yaml_new(config_file, output_file):
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

    if driver == None:
        print("Driver initialisation failed")
        return

    # Visit the specified URL
    driver.get(url)

    # Create WebDriverWait object outside the loop
    wait = WebDriverWait(driver, 10)

    for step in steps:
        # Decide what type of step it is
        steptype = step['type']

        # Send it off to another function to implement this step? That feels fairly sane.
        # Decide how to handle return values and actions.


    # Things to be resolved:
    # Do we, or do we now need recursion? It'll be clunky if we don't have it.
    # learn how to use dictionaries, that is how the variables will be created and assigned to on the fly.

