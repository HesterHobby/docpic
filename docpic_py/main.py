import os

from docpic_py.docpic import run_docpic
from docpic_py.selenium_processor import take_screenshot_from_yaml_file

# Run docpic example
if __name__ == '__main__':

    print(f"\nworking directory is {os.getcwd()}")
    # Uncomment the relevant section(s) to run.

    # Run from yaml:
    take_screenshot_from_yaml_file("../yaml_and_markup/logintest.dp.yaml")

    # Run from md, specify outfile and image folder:
    # run_docpic("../yaml_and_markup/example_md_config.md", "out/test.md", "img")

    # Run from md, specify outfile only:
    # run_docpic("../yaml_and_markup/example_md_config.md", "out/test.md")

    # Run from md, specify input only:
    # run_docpic("../yaml_and_markup/example_md_config.md")

    # Run from md, overwrite existing (copy md first):
    # run_docpic("yaml_and_markup/example_md_config_copy.md", overwrite_existing=True)
