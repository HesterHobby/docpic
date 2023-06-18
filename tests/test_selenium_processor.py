# import os
# import sys
#
# import pytest
# from selenium.webdriver.remote.webelement import WebElement
# from python.selenium_processor import get_element_from_varname
# from unittest.mock import patch
#
# # Add the project root directory to the Python module search path
# current_dir = os.path.dirname(os.path.realpath(__file__))
# project_root = os.path.abspath(os.path.join(current_dir, ".."))
# sys.path.insert(0, project_root)
#
#
# def test_get_element_from_varname_existing_element():
#     # Arrange
#     varname = "element1"
#     element1 = WebElement(parent='dummy_parent', id_='dummy_id')  # Create a dummy WebElement for testing
#     module_vars = {"element1": element1}
#
#     with patch("docpic.selenium_processor.module_vars", module_vars):
#         # Act
#         result = get_element_from_varname(varname)
#
#         # Assert
#         assert result == element1
#
#
# def test_get_element_from_varname_nonexistent_element():
#     # Arrange
#     varname = "element2"
#     module_vars = {}
#
#     with patch("docpic.selenium_processor.module_vars", module_vars):
#         # Act and Assert
#         with pytest.raises(KeyError):
#             get_element_from_varname(varname)
