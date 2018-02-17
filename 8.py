__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__license__ = "Apache 2.0"
__version__ = "1.0"
__copyright__ = "Copyright 2018, Eugene Alekseev"
__email__ = "example@gmail.com"
__status__ = "production"

import argparse
import itertools
import re


def main():
    argparser = argparse.ArgumentParser(description="Parser to handle input words")
    argparser.add_argument("--words", "-w", action="store", dest="words", nargs="*")
    args = argparser.parse_args()
    words = [re.findall("\w+", word) for word in args.words]
    words = itertools.chain.from_iterable(words)
    words = list(words)

    sorted_words = sorted(words)
    sorted_words = ", ".join(sorted_words)
    print(sorted_words)

if __name__ == "__main__":
    main()