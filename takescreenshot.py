from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import yaml
from selenium import webdriver
from yaml_validator import validate_yaml_schema

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

    # Set the path to chromedriver executable
    chromedriver_path = 'path/to/chromedriver'

    # Set the options for ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)

    # Launch ChromeDriver with the specified path and options
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

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

    # Take a screenshot and save it to the output file
    driver.save_screenshot(output_file)

    # Close the browser
    driver.quit()
