from html2image import Html2Image
from tap import Tap
import random

from elements import *

class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


def main():
    element = Element(tag='div')
    print(element.to_html())

if __name__ == '__main__':
    main()