import argparse


class Cache:
    __instance = None

    def __init__(self):
        self.memory = dict()

    @staticmethod
    def get_instance():
        if Cache.__instance is None:
            Cache.__instance = Cache()
            return Cache.__instance
        else:
            return Cache.__instance

    def __dict__(self):
        return self.memory

    def __str__(self):
        return str(self.memory)

    def __repr__(self):
        return repr(self.memory)

    def __getattr__(self, key):
        return self.memory[key]

    def __iter__(self):
        return iter(self.memory)


cache = Cache.get_instance()


def memoize(func):
    global cache

    def wrapped(n):
        if n not in cache.memory:
            cache.memory[n] = func(n)
        return cache.memory[n]
    return wrapped

@memoize
def factorial(n):
    if n in (0, 1):
        return 1
    else:
        return n * factorial(n-1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--numbers", action="store", default=[], nargs="*", dest="numbers")
    parsed = parser.parse_args()
    for number in parsed.numbers:
        print(factorial(int(number)))

if __name__ == "__main__":
    main()