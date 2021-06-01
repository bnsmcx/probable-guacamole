"""
FILE:       unit-test.py
DATE:       22 MAY 2021
AUTHOR:     Ben Simcox
PROJECT:    probable-guacamole
PURPOSE:    Tests markdown_to_html.py
"""
import compile_md_to_html as m2h


def main():
    """main function"""
    compiler = m2h.Compiler("test.md")
    print("\nOUTPUT:\n\n" + compiler.get_html())


if __name__ == '__main__':
    main()
