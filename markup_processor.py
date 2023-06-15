# This module is intended to process incoming .md files and pass relevant yaml back.
# Note that for the moment we're assuming that what's between the docpic tags is yaml; this may change.
import re
from typing import List


def parse_markup(markdown_text: str):
    # Rather simplistically, let's give it [docpic] [/docpic] tags
    docpic_tag_pattern = r'\[docpic\](.*?)\[/docpic\]'

    docpic_sections = re.findall(docpic_tag_pattern, markdown_text, re.DOTALL)

    return docpic_sections


def read_file(infile: str):
    try:
        with open(infile, 'r') as file:
            markdown_text = file.read()
            return markdown_text
    except FileNotFoundError:
        print(f"Error: File '{infile}' not found.")
        return


def process_markup(markdown_text: str, new_sections: List[str]):
    # Construct the regex pattern to match [docpic]..[/docpic] blocks
    docpic_tag_pattern = r'\[docpic\](.*?)\[/docpic\]'

    # Replace [docpic]..[/docpic] blocks with new text
    replaced_content = re.sub(docpic_tag_pattern, lambda match: new_sections.pop(0), markdown_text, flags=re.DOTALL)

    return replaced_content


def write_file(new_content: str, filename: str):
    # Write the modified content back to the input file
    try:
        with open(filename, 'w') as file:
            file.write(new_content)
    except Exception as e:
        # Handle the exception or log the error message
        print(f"Error occurred while writing to file: {e}")
        raise

