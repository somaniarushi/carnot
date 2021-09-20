<h1 align='center'>Carnot: The Browser Engine 🚒</h1>

Carnot is a toy browser engine, written entirely in Python. It parses through HTML and CSS files as strings, then combines the two in a DOM structure and paints it onto a window. As such, Carnot does not follow the HTML/CSS standard. Instead, it attempts a minor subset of these, with the goal of understanding how actual browsers work. 

### List of Improvements
- Non-comprehensive testing.
- Currently only supports one tag name and one ID per element.
- No stylesheet cascading.
- No CSS selector chaining.
- No floats, no absolute positioning, and no fixed positioning.

## Running Locally
Since this project is built completely from scratch, it does not use any dependencies. Fork this project, then take a look at `test_html_parser.py`, `test_css_parser.py` and `test_style_tree.py` to view how parsers operate.

## Contributing
If you want to open 

Inspired by [Matt Brubek's Robinson Engine](https://github.com/mbrubeck/robinson).
