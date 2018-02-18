__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = "v1.0"

import argparse
import itertools
import re


def main():
    argparser = argparse.ArgumentParser(description="Parser that handles input text")
    argparser.add_argument("--text", "-t", action="store", nargs="*", dest="text")
    text = argparser.parse_args().text
    text = itertools.chain.from_iterable(text)
    text = " ".join(text)

    digits = re.findall("\d", text)
    letters = re.findall("[a-zA-Z]", text)

    print("digits: ", len(digits))
    print("letters: ", len(letters))


if __name__ == "__main__":
    main()