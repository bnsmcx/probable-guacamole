"""
FILE:       test_MarkdownToHTML.py
DATE:       22 MAY 2021
AUTHOR:     Ben Simcox
PROJECT:    probable-guacamole
PURPOSE:    Tests markdown_to_html.py
"""
import markdown_to_html as m2h


def main():
    """main function"""
    for line in m2h.get_html("test.md"):
        if line:
            print(line)
    # print(m2h.get_preview("test.md"))


if __name__ == '__main__':
    main()
