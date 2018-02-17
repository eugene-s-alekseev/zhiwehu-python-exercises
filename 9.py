__author__ = "Eugene Alekseev"
__version__ = 1.0
__status__ = "production"


def main():
    strings = list()
    while True:
        input_line = input()
        if input_line:
            strings.append(input_line)
        else:
            break

    strings = [line.upper() for line in strings]
    print(strings)

if __name__ == "__main__":
    main()