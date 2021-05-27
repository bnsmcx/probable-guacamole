"""
FILE:       markdown_to_html.py
AUTHOR:     Ben Simcox
PROJECT:    probable-guacamole
PURPOSE:    Compiles Markdown documents to HTML.
            Two public functions:
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
    return "<blockquote>" + quote + "</blockquote>"


def _parse_paragraph(line: list) -> str:
    """parse markdown to return html paragraph"""
    paragraph = _parse_inline(line)
    return "<p>" + paragraph + "</p>"


def _parse_list(line: list) -> str:
    """parse markdown, return html unordered list"""
    return "\t<li>" + _parse_inline(line) + "</li>"


def _process_lines(markdown_lines: list) -> list:
    """parse a line of markdown to html"""

    html_lines = []

    while markdown_lines:
        line = markdown_lines.pop(0)

        if line == '\n':
            continue

        line = line.strip().split()
        first_token = line[0]
        special_line = line[1:]

        if re.fullmatch("#+", first_token):
            html_lines.append(_parse_heading(special_line, first_token))

        elif first_token == '>':
            html_lines.append(_parse_blockquote(special_line))

        elif first_token in ['-', '*']:
            unordered_list = ["<ul>", _parse_list(special_line)]
            while len(markdown_lines) > 0:
                if markdown_lines[0] == "\n" or markdown_lines[0].split()[0] not in ['-', '*']:
                    break
                else:
                    unordered_list.append(_parse_list(markdown_lines.pop(0).strip().split()[1:]))
            unordered_list.append("</ul>")
            for item in unordered_list:
                html_lines.append(item)

        elif re.fullmatch("[0-9]+\\.", first_token):
            ordered_list = ["<ol>", _parse_list(special_line)]
            while len(markdown_lines) > 0:
                if markdown_lines[0] == "\n" or not re.fullmatch("[0-9]+\\.", markdown_lines[0].split()[0]):
                    break
                else:
                    ordered_list.append(_parse_list(markdown_lines.pop(0).strip().split()[1:]))
            ordered_list.append("</ol>")
            for item in ordered_list:
                html_lines.append(item)

        elif re.fullmatch("[-=]{3,}", first_token):
            html_lines.append("<hr />")

        elif re.fullmatch("<.*", first_token):
            pass

        else:
            html_lines.append(_parse_paragraph(line))

    return html_lines


def _read_markdown_file(markdown_file_path: str) -> list:
    """read the markdown file into a list of lines"""
    lines = []
    try:
        with open(markdown_file_path) as file:
            for line in file.readlines():
                lines.append(line)
        return lines
    except FileNotFoundError:
        print("Someday I'll handle this file not found thing.")
        return lines


def get_html(markdown_file_path: str) -> list:
    """accepts the path to a markdown file and compiles the content to HTML"""
    markdown_lines = _read_markdown_file(markdown_file_path)
    return _process_lines(markdown_lines)


def get_preview(markdown_file_path: str) -> dict:
    """accepts the path to a markdown file and returns a dictionary containing preview elements"""
    preview = {"title": "", "date": "", "preview": ""}
    return preview
