import re


def format_file_name(name: str) -> str:
    name = name.replace(" ", "-")
    name = re.sub(r'[\\/:*?"<>|]+', '', name)
    return name
