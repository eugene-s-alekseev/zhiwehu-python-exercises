__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = 1.0

import argparse
import itertools
import re


def main():
    parser = argparse.ArgumentParser(description="Input arguments handler")
    parser.add_argument("--words", "-w", action="store", nargs="*", dest="words")
    args = parser.parse_args()
    words = [re.findall("\w+", word) for word in args.words]
    words = itertools.chain.from_iterable(words)
    words = [word.lower() for word in words]

    print(" ".join(sorted(set(words))))

if __name__ == "__main__":
    main()