# The docpic module ties everything together.
from datetime import datetime

import click
import os

from markup_processor import parse_markup, read_file, process_markup, write_file
from selenium_processor import take_screenshot_from_yaml


@click.command()
@click.option("--infile", help="The location of your infile, relative to the current folder.")
@click.option("--outfile", help="Output file, relative to the current folder.")
@click.option("--img-dir", default="assets", help="Output folder, relative to the output folder. Defaults to 'assets'.")
@click.option("--overwrite-existing", is_flag=True, help="When specified, this overwrites the [docpic]..[/docpic] "
                                                         "sections in your input file.")
def docpic(infile: str, outfile: str = None, img_dir: str = "assets", overwrite_existing: bool = False):
    run_docpic(infile, outfile, img_dir, overwrite_existing)


def run_docpic(infile: str, outfile: str = None, img_dir: str = "assets", overwrite_existing: bool = False) -> object:
    # Process the input arguments
    if overwrite_existing:
        outfile = infile

    if not outfile:
        # Convert the input file path to the platform-specific format
        infile = os.path.normpath(infile)

        # Extract the folder names from the input file path
        folders = infile.split(os.path.sep)
        output_folder_path = os.path.join("out", *folders[1:-1])

        # Generate the output file path
        outfile = os.path.join(output_folder_path, folders[-1])
        outfile = os.path.splitext(outfile)[0] + ".generated." + datetime.now().strftime("%Y%m%d_%H%M") + ".md"
    else:
        output_folder_path = os.path.dirname(outfile)

    docpic_img_dir = os.path.join(output_folder_path, img_dir)

    # Does the input file have any docpic tags?
    in_text = read_file(infile)
    yaml_array = parse_markup(in_text)

    if len(yaml_array) == 0:
        print("No docpic sections found in document")
        return

    image_tags = []

    for yaml_section in yaml_array:
        screenshot_result = take_screenshot_from_yaml(yaml_section, docpic_img_dir)

        print("Adding docpic: " + screenshot_result["outfile"].replace("\\", "/") +
              ", with alt text: " + screenshot_result["alt_text"] + ".")

        image_tag = "![" + screenshot_result["alt_text"] + "](" + img_dir + "/" + screenshot_result["outfile"].\
            replace("\\", "/") + ")"

        image_tags.append(image_tag)

    section_count = len(image_tags)

    # Now replace the content with the results
    new_content = process_markup(in_text, image_tags)
    write_file(new_content, outfile)

    print("Replaced " + str(section_count) + " docpic tag(s) with image tags.")
    print("Output is in " + outfile)


if __name__ == '__main__':
    docpic()
