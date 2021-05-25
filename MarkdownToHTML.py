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
import re


def _contains_inline_syntax(word: str) -> bool:
    """check for bold/italic/code and return the right tags"""
    return re.match("[`\\*]{1,3}", word)


def _parse_inline_syntax(word: str) -> str:
    """return appropriate html tag for code/bold/italics"""
    if re.match("(?<!\\*)\\*(?!\\*)", word):
        word = re.sub("^(?<!\\*)\\*(?!\\*)", "<em>", word)
        word = re.sub("(?<!\\*)\\*(?!\\*)$", "</em>", word)
        return word
    elif re.match("(?<!\\*)\\*{2}(?!\\*)", word):
        word = re.sub("^(?<!\\*)\\*{2}(?!\\*)", "<strong>", word)
        word = re.sub("(?<!\\*)\\*{2}(?!\\*)$", "</strong>", word)
        return word
    elif re.match("(?<!\\*)\\*{3}(?!\\*)", word):
        word = re.sub("^(?<!\\*)\\*{3}(?!\\*)", "<strong><em>", word)
        word = re.sub("(?<!\\*)\\*{3}(?!\\*)$", "</em></strong>", word)
        return word
    elif re.match("`", word):
        word = re.sub("^`", "<code>", word)
        word = re.sub("`$", "</code>", word)
        return word


def _parse_heading(line: str) -> str:
    """parse markdown to return html heading"""
    heading_level = len(line.split()[0])
    opening_tag = "<h" + str(heading_level) + ">"
    heading_text = ""
    closing_tag = "</h" + str(heading_level) + ">"

    for word in line.strip().split()[1:]:
        if _contains_inline_syntax(word):
            heading_text += _parse_inline_syntax(word) + " "
        else:
            heading_text += word + " "

    return opening_tag + heading_text.strip() + closing_tag


def _process_line(line: str) -> str:
    """parse a line of markdown to html"""
    if line == '\n':
        return

    first_token = line.split()[0]

    if re.fullmatch("#+", first_token):
        return _parse_heading(line)
    elif first_token == '>':
        pass
    elif first_token in ['-', '*']:
        pass
    elif re.fullmatch("[0-9]+\\.", first_token):
        pass
    elif re.fullmatch("[-=]{3,}", first_token):
        pass
    elif re.fullmatch("<.*", first_token):
        pass
    else:
        pass


def get_html(markdown_file_path: str) -> list:
    """accepts the path to a markdown file and compiles the content to HTML"""
    html = []
    try:
        with open(markdown_file_path) as f:
            for line in f.readlines():
                html.append(_process_line(line))
        return html
    except FileNotFoundError:
        return "File not found."


def get_preview(markdown_file_path: str) -> dict:
    """accepts the path to a markdown file and returns a dictionary containing preview elements"""
    preview = {"title": "", "date": "", "preview": ""}
    return preview
