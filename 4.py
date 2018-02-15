import argparse
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", action="store", dest="numbers", nargs="*")
    args = parser.parse_args()
    print(tuple(re.findall("\d+", number)[0] for number in args.numbers))
    print(list(re.findall("\d+", number)[0] for number in args.numbers))


if __name__ == "__main__":
    main()