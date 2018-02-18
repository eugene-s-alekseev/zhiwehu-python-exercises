__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version__ = "v1.0"

import argparse
import logging
import re
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


def is_valid_password(password):
    if len(password) < 6:
        return False
    if len(password) > 12:
        return False
    if not re.findall("[a-z]+", password):
        return False
    if not re.findall("\d+", password):
        return False
    if not re.findall("[A-Z]+", password):
        return False
    if not re.findall("[$#@]+", password):
        return False
    return True


def main():
    argparser = argparse.ArgumentParser(description="Parser that handles input arguments")
    argparser.add_argument("--passwords", "-p", action="store", dest="passwords", nargs="*")
    passwords = argparser.parse_args().passwords
    passwords = [password.rstrip(",") for password in passwords]
    valid_passwords = list(filter(is_valid_password, passwords))

    logger.info(", ".join(valid_passwords))


if __name__ == "__main__":
    main()