from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


def initialize_driver(webdriver_options):
    options = webdriver.ChromeOptions()
    #options.headless = False

    #  DeprecationWarning: headless property is deprecated, instead use add_argument('--headless') or add_argument('--headless=new')
    if 'headless' in webdriver_options and webdriver_options['headless']:
        #options.headless = True
        options.add_argument('--headless')

    if webdriver_options is not None:
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
        print("Failed to initialize webdriver:", e)
        return None
