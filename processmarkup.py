# This module is intended to process incoming .md files and pass relevant yaml back.
# Note that for the moment we're assuming that what's between the docpic tags is yaml; this may change.
import re


def process_markup_file(infile: str):
    try:
        with open(infile, 'r') as file:
            markdown_text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{infile}' not found.")
        return []

    # Rather simplistically, let's give it [docpic] [/docpic] tags
    docpic_tag_pattern = r'\[docpic\](.*?)\[/docpic\]'

    docpic_sections = re.findall(docpic_tag_pattern, markdown_text, re.DOTALL)

    return docpic_sections
