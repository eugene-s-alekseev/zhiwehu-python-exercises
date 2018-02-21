__author__ = "Eugene Alekseev"
__maintainer__ = "Eugene Alekseev"
__version___ = "v1.0"


def main():
    for a in globals():
        print(a, a.__doc__)
        print("-".center(50, "-"))


if __name__ == "__main__":
    main()