from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager  # I am using version 3.8.6 of webdriver_manager, as newer


# versions fail to download chrome for me.


def initialize_driver(webdriver_options):
    options = webdriver.ChromeOptions()

    if webdriver_options and 'headless' in webdriver_options and webdriver_options['headless']:
        options.add_argument('--headless')

    if webdriver_options:
        for option, value in webdriver_options.items():
            if option != 'headless':
                options.add_argument(f"--{option}={value}")

    try:
        # Add any additional options to the webdriver options object
        # For example, you can set the window size:
        # options.add_argument("--window-size=1200x800")

        # Initialize the webdriver with the configured options
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except WebDriverException as e:
        print("\nFailed to initialize webdriver:", e)
        return None
