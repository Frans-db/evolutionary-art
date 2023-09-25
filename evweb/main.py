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
    properties = [
        RealProperty(name='width', min_value=0, max_value=100, unit='rem'),
        RealProperty(name='height', min_value=0, max_value=100, unit='rem'),
        RealProperty(name='padding', min_value=0, max_value=100, unit='rem'),
        RealProperty(name='margin', min_value=0, max_value=100, unit='rem'),
        RGBProperty(name='background-color')
    ]
    element.properties.extend(properties)
    print(element.to_html())

if __name__ == '__main__':
    main()