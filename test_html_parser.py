from html_parser import parse

def run_test_files():
    with open('tests/html/html_test_1.html') as f:
        parse(f.read())

def main():
    run_test_files()

if __name__ == "__main__":
    main()