__author__ = "Eugene Alekseev"

import unittest


class InputOutString:
    def __init__(self):
        self.input = ""

    def get_string(self):
        input_string = input("Please type something: ")
        self.input = input_string

    def print_string(self):
        print(self.input)


def main():
    input_out_string = InputOutString()
    input_out_string.get_string()
    input_out_string.print_string()


if __name__ == "__main__":
    main()