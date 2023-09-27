from tap import Tap

from elements import *

class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


def main():
    element = get_default_element()
    print(element.to_html())

if __name__ == '__main__':
    main()