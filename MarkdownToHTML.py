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
    """check for bold/italic/code markdown syntax"""
    syntax_flags = ['*', '**', '***', '`']

    for flag in syntax_flags:
        if flag in word:
            return True

    return False


def _parse_inline_syntax(word: str) -> str:
    """return appropriate html tag for code/bold/italics"""
    if word[-1] in ['.', '!', '?', ',']:
        return _parse_inline_syntax(word[:-1]) + "."

    word = re.sub("^(?<!\\*)\\*(?!\\*)", "<em>", word)
    word = re.sub("(?<!\\*)\\*(?!\\*)$", "</em>", word)
    word = re.sub("^(?<!\\*)\\*{2}(?!\\*)", "<strong>", word)
    word = re.sub("(?<!\\*)\\*{2}(?!\\*)$", "</strong>", word)
    word = re.sub("^(?<!\\*)\\*{3}(?!\\*)", "<strong><em>", word)
    word = re.sub("(?<!\\*)\\*{3}(?!\\*)$", "</em></strong>", word)
    word = re.sub("^`", "<code>", word)
    word = re.sub("`$", "</code>", word)
    return word


def _parse_inline(line: list) -> str:
    """scrubs a line for inline syntax"""
    text = ""
    for word in line:
        if _contains_inline_syntax(word):
            text += _parse_inline_syntax(word) + " "
        else:
            text += word + " "
    return text.strip()


def _parse_heading(line: list, first_token: str) -> str:
    """parse markdown to return html heading"""
    heading_level = len(first_token)
    opening_tag = "<h" + str(heading_level) + ">"
    heading_text = _parse_inline(line)
    closing_tag = "</h" + str(heading_level) + ">"

    return opening_tag + heading_text + closing_tag


def _parse_blockquote(line: list) -> str:
    """parse markdown to return html blockquote"""
    quote = _parse_inline(line)
    return "<p>" + quote + "</p>"


def _parse_paragraph(line: list) -> str:
    """parse markdown to return html paragraph"""
    paragraph = _parse_inline(line)
    return paragraph


def _process_line(line: str) -> str:
    """parse a line of markdown to html"""
    if line == '\n':
        return

    line = line.strip().split()
    first_token = line[0]
    line = line[1:]

    if re.fullmatch("#+", first_token):
        return _parse_heading(line, first_token)
    elif first_token == '>':
        return _parse_blockquote(line)
    elif first_token in ['-', '*']:
        pass
    elif re.fullmatch("[0-9]+\\.", first_token):
        pass
    elif re.fullmatch("[-=]{3,}", first_token):
        return "<hr />"
    elif re.fullmatch("<.*", first_token):
        pass
    else:
        return _parse_paragraph(line)


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
