"""
FILE:       compile_md_to_html.py
AUTHOR:     Ben Simcox
PROJECT:    probable-guacamole
PURPOSE:    Recursively compile markdown to html
"""
import re


class Compiler:
    """Compiler class manages markdown to html compiling"""

    def __init__(self, markdown_file_location: str):
        """Initialize attributes"""
        self.md_tokens = self._read_markdown(markdown_file_location)  # list
        self.html = self._compile()  # str
        # self.preview = self._get_preview()  # str

    @staticmethod
    def _read_markdown(markdown_file_location: str) -> list:
        """Reads a markdown file and returns a list of lines"""
        with open(markdown_file_location) as file:
            return file.readlines()

    def get_html(self):
        """return the html"""
        return self.html

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
            return self._parse_heading(line, len(line[0]))
        else:
            return self._parse_paragraph(line)

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

    def _parse_heading(self, line: list, level: int) -> str:
        """process an html heading"""
        heading = "<h" + str(level) + ">"
        line = line[1:]
        while line:
            token = line.pop(0)
            heading += self._parse_inline_syntax(token) + " "
        return heading.rstrip() + "</h" + str(level) + ">\n"

    @staticmethod
    def _parse_inline_syntax(token: str) -> str:
        """check if a token contains markdown syntax"""
        """Order of these statements is meaningful"""

        """Handle bold and italic"""
        if re.search("^\\*{3}.+\\*{3}$", token):
            return "<bold><em>" + token[3:-3] + "</em></bold>"
        if re.search("^\\*{3}", token):
            return "<bold><em>" + token[3:]
        if re.search("\\*{3}$", token):
            return token[:-3] + "</em></bold>"

        """Handle bold"""
        if re.search("^\\*{2}.+\\*{2}$", token):
            return "<bold>" + token[2:-2] + "</bold>"
        if re.search("^\\*{2}", token):
            return "<bold>" + token[2:]
        if re.search("\\*{2}$", token):
            return token[:-2] + "</bold>"

        """Handle Italics"""
        if re.search("^\\*.+\\*$", token):
            return "<em>" + token[1:-1] + "</em>"
        if re.search("^\\*", token):
            return "<em>" + token[1:]
        if re.search("\\*$", token):
            return token[:-1] + "</em>"
        return token

    def _parse_paragraph(self, line: list) -> str:
        """Parse markdown return html paragraph"""
        paragraph_text = ""
        for word in line:
            paragraph_text += self._parse_inline_syntax(word) + " "
        return "<p>" + paragraph_text.strip() + "</p>\n"
