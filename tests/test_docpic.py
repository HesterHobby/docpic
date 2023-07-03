# A single test to make sure it still runs.
import pytest
import subprocess

from docpic_py.docpic import run_docpic
from os import path


@pytest.mark.slow
def test_docpic_with_params(tmp_path):
    outfile = tmp_path / "test.md"
    out_image = tmp_path / "img/test.png"
    run_docpic("../yaml_and_markup/example_md_config.md", str(outfile), "img")
    assert path.exists(outfile)
    assert path.exists(out_image)


# Note this only runs from the command line, the IDE gives a weird error.
def test_run_from_command_line():
    # Define the command to run your process
    command = "python ../docpic_py/docpic.py --infile ../yaml_and_markup/example_md_config.md --img-dir assets/"

    # Run the command and capture the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Assert the expected output or behavior
    assert result.returncode == 0  # Check if the process exited successfully
    assert "Output is in" in result.stdout  # Check if the expected output message is present
