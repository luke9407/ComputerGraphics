import random
from util.vector import *


class BSP:
    def __init__(self):
        self.root = None
        self.right = None
        self.left = None

    def build(self, surfaces):
        if len(surfaces) == 0:
            return None

        random.shuffle(surfaces)
        surface = surfaces.pop()

        self.root = surface

        left, right = self.divide(self.root, surfaces)
        self.left = BSP().build(left)
        self.right = BSP().build(right)

        return self

    @staticmethod
    def divide(parent, surfaces):
        left = right = []
        print(parent)

        return left, right
