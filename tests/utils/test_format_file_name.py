from app.utils import format_file_name


def test_format_file_name_replaces_spaces_with_hyphens():
    assert format_file_name("Hello World") == "Hello-World"


def test_format_file_name_removes_special_characters():
    assert format_file_name("Hello/World:Test") == "HelloWorldTest"


def test_format_file_name_with_empty_string():
    assert format_file_name("") == ""


def test_format_file_name_with_only_special_characters():
    assert format_file_name("\\/:*?\"<>|") == ""


def test_format_file_name_with_only_spaces():
    assert format_file_name("     ") == "-----"
