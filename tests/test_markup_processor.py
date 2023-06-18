import pytest

from docpic_py.markup_processor import parse_markup, read_file, process_markup, write_file


def test_parse_markup_with_single_section():
    markdown_text = "[docpic]\n# Title\n\nThis is some **bold** and *italic* text.\n\n- Item 1\n- Item 2\n[/docpic]"
    result = parse_markup(markdown_text)
    assert len(result) == 1
    assert result[0] == "\n# Title\n\nThis is some **bold** and *italic* text.\n\n- Item 1\n- Item 2\n"


def test_parse_markup_with_multiple_sections():
    markdown_text = "[docpic]\n## Section 1\n\nThis is the first section.\n[/docpic][docpic]\n## Section 2\n\nThis is the second section.\n[/docpic][docpic]\n## Section 3\n\nThis is the third section.\n[/docpic]"
    result = parse_markup(markdown_text)
    assert len(result) == 3
    assert result[0] == "\n## Section 1\n\nThis is the first section.\n"
    assert result[1] == "\n## Section 2\n\nThis is the second section.\n"
    assert result[2] == "\n## Section 3\n\nThis is the third section.\n"


def test_parse_markup_with_no_sections():
    markdown_text = "This is a normal text without any docpic sections"
    result = parse_markup(markdown_text)
    assert len(result) == 0


def test_read_existing_file(tmp_path):
    # Create a temporary file with some content
    test_file = tmp_path / "test_file.txt"
    content = "This is a test file."
    test_file.write_text(content)

    # Test reading an existing file
    result = read_file(test_file)
    assert result == content


def test_read_nonexistent_file():
    # Test reading a non-existent file
    result = read_file("nonexistent.txt")
    assert result is None


def test_process_markup():
    markdown_text = "[docpic]Image 1[/docpic] Some text [docpic]Image 2[/docpic]"
    new_sections = ["![alt text 1](image1.jpg)", "![alt text 2](image2.jpg)"]

    result = process_markup(markdown_text, new_sections)

    expected_result = "![alt text 1](image1.jpg) Some text ![alt text 2](image2.jpg)"
    assert result == expected_result


def test_process_markup_insufficient_sections():
    markdown_text = "[docpic]Image 1[/docpic] Some text [docpic]Image 2[/docpic]"
    new_sections = ["![alt text 1](image1.jpg)"]

    with pytest.raises(IndexError):
        process_markup(markdown_text, new_sections)


def test_process_markup_excess_sections():
    markdown_text = "[docpic]Image 1[/docpic] Some text [docpic]Image 2[/docpic]"
    new_sections = ["![alt text 1](image1.jpg)", "![alt text 2](image2.jpg)", "![alt text 3](image3.jpg)"]

    result = process_markup(markdown_text, new_sections)

    expected_result = "![alt text 1](image1.jpg) Some text ![alt text 2](image2.jpg)"
    assert result == expected_result


def test_write_file(tmp_path):
    # Create a temporary file
    test_file = tmp_path / "test_file.txt"

    # Write some content to the file
    content = "Initial content"
    write_file(content, str(test_file))

    # Read the file and verify the content
    with open(test_file, 'r') as file:
        assert file.read() == content

    # Update the file content
    new_content = "Updated content"
    write_file(new_content, str(test_file))

    # Read the file again and verify the updated content
    with open(test_file, 'r') as file:
        assert file.read() == new_content


def test_write_file_exception(tmp_path):
    # Create a temporary file
    test_file = tmp_path / "test_file.txt"

    # Specify a non-existent directory path
    non_existent_dir = tmp_path / "non_existent"

    # Ensure an exception is raised
    with pytest.raises(Exception) as exc_info:
        write_file("Content", str(non_existent_dir / "test_file.txt"))
