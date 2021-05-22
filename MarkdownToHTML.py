"""
FILE:       MarkdownToHTML.py
DATE:       22 MAY 2021
AUTHOR:     Ben Simcox
PROJECT:    probable-guacamole
PURPOSE:    Compiles Markdown documents to HTML.
            Has two public functions:
                getHTML()
                getPreview()
"""


def _process(line: str) -> str:
    if line[0] == "\n":
        return
    if line[0] == "#":
        line = line.strip("#").strip()
        return "<h1>" + line + "</h1>"
    elif line[0] == "<":
        return "Process an html tag."
    else:
        line = line.strip()
        return "<p>" + line + "</p>"


def get_html(markdown_file_path: str) -> list:
    """accepts the path to a markdown file and compiles the content to HTML"""
    html = []
    try:
        with open(markdown_file_path) as f:
            for line in f.readlines():
                html.append(_process(line))
        return html
    except FileNotFoundError:
        return "File not found."


def get_preview(markdown_file_path: str) -> dict:
    """accepts the path to a markdown file and returns a dictionary containing preview elements"""
    preview = {"title": "", "date": "", "preview": ""}
    return preview
