# The docpic module ties everything together.
import click
import os

from processmarkup import process_markup_file
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
    yaml_array = process_markup_file(infile)

    if len(yaml_array) == 0:
        print("No docpic sections found")
        return

    for yaml_section in yaml_array:
        screenshot_result = take_screenshot_from_yaml(yaml_section, img_dir)

        print("Results are: outfile: " + screenshot_result["outfile"] +
              ", alt text: " + screenshot_result["alt_text"] + ".")
        # Store the output in buffer - file location, alt text.

    # ToDo: Modify the input file and either overwrite or write to new file, depending on user choice.


if __name__ == '__main__':
    docpic()