"""
FILE:       compile_md_to_html.py
AUTHOR:     Ben Simcox
PROJECT:    probable-guacamole
PURPOSE:    Recursively compile markdown to html
"""
import re


def _parse_bold_italic(token: str) -> str:
    """Handle bold and italic"""
    if re.search("^\\*{3}.+\\*{3}$", token):
        return "<bold><em>" + token[3:-3] + "</em></bold>"
    if re.search("^\\*{3}", token):
        return "<bold><em>" + token[3:]
    if re.search("\\*{3}$", token):
        return token[:-3] + "</em></bold>"
    return token


def _parse_bold(token: str) -> str:
    """Handle bold"""
    if re.search("^\\*{2}.+\\*{2}$", token):
        return "<bold>" + token[2:-2] + "</bold>"
    if re.search("^\\*{2}", token):
        return "<bold>" + token[2:]
    if re.search("\\*{2}$", token):
        return token[:-2] + "</bold>"
    return token


def _parse_italic(token: str) -> str:
    """Handle Italics"""
    if re.search("^\\*.+\\*$", token):
        return "<em>" + token[1:-1] + "</em>"
    if re.search("^\\*", token):
        return "<em>" + token[1:]
    if re.search("\\*$", token):
        return token[:-1] + "</em>"
    return token


def _read_markdown(markdown_file_location: str) -> list:
    """Reads a markdown file and returns a list of lines"""
    with open(markdown_file_location) as file:
        return file.readlines()


def _parse_code_block(token: str) -> str:
    """Handle code blocks"""
    if re.search("^`.+`$", token):
        return "<code>" + token[1:-1] + "</code>"
    if re.search("^`", token):
        return "<code>" + token[1:]
    if re.search("`$", token):
        return token[:-1] + "</code>"
    return token
    pass


def _parse_inline_syntax(token: str) -> str:
    """check for and handle inline syntax, statement order is meaningful"""
    if re.search("^\\*{3}", token) or re.search("\\*{3}$", token):
        return _parse_bold_italic(token)
    if re.search("^\\*{2}", token) or re.search("\\*{2}$", token):
        return _parse_bold(token)
    if re.search("^\\*", token) or re.search("\\*$", token):
        return _parse_italic(token)
    if re.search("^`", token) or re.search("`$", token):
        return _parse_code_block(token)
    return token


def _parse_paragraph(line: list) -> str:
    """Parse markdown return html paragraph"""
    paragraph_text = ""
    for word in line:
        paragraph_text += _parse_inline_syntax(word) + " "
    return "<p>" + paragraph_text.strip() + "</p>\n"


def _parse_heading(line: list, level: int) -> str:
    """process an html heading"""
    heading = "<h" + str(level) + ">"
    line = line[1:]
    while line:
        token = line.pop(0)
        heading += _parse_inline_syntax(token) + " "
    return heading.rstrip() + "</h" + str(level) + ">\n"


class Compiler:
    """Compiler class manages markdown to html compiling"""

    def __init__(self, markdown_file_location: str):
        """Initialize attributes"""
        self.md_tokens = _read_markdown(markdown_file_location)  # list
        self.html = self._compile()  # str
        self.preview = self._get_preview()  # str

    def get_html(self):
        """return the html"""
        return self.html

    def get_preview(self):
        """return the preview"""
        return self.preview

    def _compile(self):
        """Entry point where the parsing of markdown begins"""
        html = ""
        while self.md_tokens:
            html += self._parse_line(self._get_next_line())
        return html

    def _parse_line(self, line: list) -> str:
        """Process a line"""
        if len(line) == 0:
            return ""
        if line[0] == "<!--":
            return self._parse_comment(line)
        if line[0] in ['#', '##', '###', '####', '#####']:
            return _parse_heading(line, len(line[0]))
        return _parse_paragraph(line)

    def _parse_comment(self, line: list) -> str:
        """process an html comment"""
        comment = ""
        if len(line) == 0:
            line = self._get_next_line()
        token = line.pop(0)
        if token != "-->":
            if token == "<!--":
                comment += token
            else:
                comment += " " + token
            comment += self._parse_comment(line)
        elif token == "-->":
            comment += " " + token + "\n"
        return comment

    def _get_next_line(self) -> list:
        """Get the next line of markdown, return it as a list"""
        return self.md_tokens.pop(0).split()

    def _get_preview(self):
        """Creates an html snippet giving a preview of the post"""
        self.preview = self.html
        return "Not implemented yet."
