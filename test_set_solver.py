#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 15:05:22 2018

@author: dominic
"""

import unittest

from set_solver import SetCard, Color, Shape, Shading


class TestSetCard(unittest.TestCase):
    """
    Unit tests for SetCard.
    """

    def testEquality(self):
        a = SetCard(number=1, color=Color.RED, shape=Shape.DIAMOND,
                    shading=Shading.NONE)
        b = SetCard(number=1, color=Color.RED, shape=Shape.DIAMOND,
                    shading=Shading.NONE)
        c = SetCard(number=2, color=Color.RED, shape=Shape.DIAMOND,
                    shading=Shading.NONE)

        self.assertEqual(a, a)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def testFindLastCardInSetNumberChange(self):
        a = SetCard(number=1, color=Color.RED, shape=Shape.DIAMOND,
                    shading=Shading.NONE)

        # Only number changes
        next_card = SetCard(number=2, color=Color.RED, shape=Shape.DIAMOND,
                            shading=Shading.NONE)
        sol = SetCard(number=3, color=Color.RED, shape=Shape.DIAMOND,
                      shading=Shading.NONE)

        last_card = a.findLastCardInSet(next_card)

        self.assertEqual(last_card, sol)

    def testFindLastCardInSetColorChange(self):
        a = SetCard(number=1, color=Color.RED, shape=Shape.DIAMOND,
                    shading=Shading.NONE)

        # Only number changes
        next_card = SetCard(number=1, color=Color.GREEN, shape=Shape.DIAMOND,
                            shading=Shading.NONE)
        sol = SetCard(number=1, color=Color.PURPLE, shape=Shape.DIAMOND,
                      shading=Shading.NONE)

        last_card = a.findLastCardInSet(next_card)

        self.assertEqual(last_card, sol)

    def testFindLastCardInSetShapeChange(self):
        a = SetCard(number=1, color=Color.RED, shape=Shape.PILL,
                    shading=Shading.NONE)

        # Only number changes
        next_card = SetCard(number=1, color=Color.RED, shape=Shape.DIAMOND,
                            shading=Shading.NONE)
        sol = SetCard(number=1, color=Color.RED, shape=Shape.SQUIGGLE,
                      shading=Shading.NONE)

        last_card = a.findLastCardInSet(next_card)

        self.assertEqual(last_card, sol)

    def testFindLastCardInSetShadingChange(self):
        a = SetCard(number=1, color=Color.RED, shape=Shape.DIAMOND,
                    shading=Shading.NONE)

        # Only number changes
        next_card = SetCard(number=1, color=Color.RED, shape=Shape.DIAMOND,
                            shading=Shading.LINES)
        sol = SetCard(number=1, color=Color.RED, shape=Shape.DIAMOND,
                      shading=Shading.FILLED)

        last_card = a.findLastCardInSet(next_card)

        self.assertEqual(last_card, sol)


if __name__ == '__main__':
    unittest.main()