from html2image import Html2Image
from tap import Tap
import random

from elements import *

class ArgumentParser(Tap):
    classlist: str
    population_size: int
    num_generations: int


def main():
    element1 = Element(tag='div')
    element1.properties.append(RGBProperty(name='background-color'))
    element2 = Element(tag='div')
    element2.properties.append(RGBProperty(name='color'))
    print(element1.properties[0])
    print(element2.properties[0])
    element1.properties[0].mutate()
    print(element1.properties[0])
    print(element2.properties[0])

if __name__ == '__main__':
    main()