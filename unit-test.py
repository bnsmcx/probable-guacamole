"""
FILE:       unit-test.py
AUTHOR:     Ben Simcox
PROJECT:    probable-guacamole
PURPOSE:    Tests md_to_html.py
"""
import md_to_html as m2h


def main():
    """main function"""
    compiler = m2h.Compiler("test.md")
    print("\nPreview:\n" + compiler.get_preview())
    print("\nFull:\n" + compiler.get_html())


if __name__ == '__main__':
    main()
