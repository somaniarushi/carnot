from css_parser import parse

#TODO: Add more tests.
def main():
    return parse('h1 { background-color: red; }}')

if __name__ == "__main__":
    print(main())