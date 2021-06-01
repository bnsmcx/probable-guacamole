"""
FILE:       compile_md_to_html.py
AUTHOR:     Ben Simcox
PROJECT:    probable-guacamole
PURPOSE:    Recursively compile markdown to html
"""


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
        else:
            return ""

    def _parse_comment(self, line: list) -> str:
        """process an html comment"""
        comment = ""
        if len(line) == 0:
            line = self._get_next_line()
        token = line.pop(0)
        print(token)
        if token != "-->":
            comment += " " + token
            comment += self._parse_comment(line)
        elif token == "-->":
            comment += " " + token + "\n"
        return comment

    def _get_next_line(self) -> list:
        """Get the next line of markdown, return it as a list"""
        return self.md_tokens.pop(0).split()
