from parsers.html_parser import parse_html
from parsers.css_parser import parse_css
from renderers.style import styled_tree

def main():
    html = parse_html('<h1>This is a test</h1>')
    css = parse_css('h1{ background-color: red;}}')
    style = styled_tree(html, css)


if __name__ == "__main__":
    main()