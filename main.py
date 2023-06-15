from selenium_processor import take_screenshot_from_yaml, take_screenshot_from_yaml_file
from docpic import run_docpic

# Run docpic example
if __name__ == '__main__':
    #take_screenshot_from_yaml_file("script_config.yaml")
    run_docpic("concept_md_config.md", "test.md")
