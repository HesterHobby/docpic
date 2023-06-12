# The docpic module ties everything together.
import click
import os

from processmarkup import parse_markup, read_file, process_markup, write_file
from takescreenshot import take_screenshot_from_yaml


@click.command()
@click.option("--infile", help="The location of your infile, relative to the current folder.")
@click.option("--outfile", help="Output file, relative to the current folder.")
@click.option("--img-dir", default="assets", help="Output folder, relative to the current folder. Defaults to 'assets'.")
@click.option("--overwrite-existing", is_flag=True, help="When specified, this overwrites the [docpic]..[/docpic] "
                                                         "sections in your input file.")
def docpic(infile: str, outfile: str = None, img_dir: str = "assets", overwrite_existing: bool = False):
    run_docpic(infile, outfile, img_dir, overwrite_existing)


def run_docpic(infile: str, outfile: str = None, img_dir: str = "assets", overwrite_existing: bool = False):
    # Process the input arguments
    if overwrite_existing:
        outfile = infile
    elif not outfile:
        outfile = os.path.splitext(infile)[0] + ".generated.md"

    # Does the input file have any docpic tags?
    in_text = read_file(infile)
    yaml_array = parse_markup(in_text)

    if len(yaml_array) == 0:
        print("No docpic sections found")
        return

    image_tags = []

    for yaml_section in yaml_array:
        screenshot_result = take_screenshot_from_yaml(yaml_section, img_dir)

        print("Adding outfile: " + screenshot_result["outfile"] +
              ", with alt text: " + screenshot_result["alt_text"] + ".")

        image_tag = "![" + screenshot_result["alt_text"] + "](" + screenshot_result["outfile"] + ")"

        image_tags.append(image_tag)

    section_count = len(image_tags)

    # Now replace the content with the results
    new_content = process_markup(in_text, image_tags)
    write_file(new_content, outfile)

    print("replaced " + str(section_count) + " docpic tag(s) with image tags.")


if __name__ == '__main__':
    docpic()