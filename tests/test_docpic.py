# A single test to make sure it still runs.
import pytest
from docpic_py.docpic import run_docpic
from os import path


@pytest.mark.slow
def test_docpic_with_params(tmp_path):
    outfile = tmp_path / "test.md"
    out_image = tmp_path / "img/test.png"
    run_docpic("../yaml_and_markup/example_md_config.md", str(outfile), "img")
    assert path.exists(outfile)
    assert path.exists(out_image)
