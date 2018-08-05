#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 14:39:56 2018

@author: dominic
"""
#%%
import enum
import itertools
import random

class Color(enum.Enum):
    RED = 1
    GREEN = 2
    PURPLE = 3


class Shading(enum.Enum):
    NONE = 1
    LINES = 2
    FILLED = 3


class Shape(enum.Enum):
    DIAMOND = 1
    PILL = 2
    SQUIGGLE = 3


class SetCard:
    """
    Basic class to represent a card.
    """

    def __init__(self, number=1, color=Color.RED, shading=Shading.NONE,
                 shape=Shape.DIAMOND):
        """
        Creates a new object.

        :param number: The number of symbols on the card.
        :param color: The color of the card as a Color enum.
        :param shading: The shading of the card as a Shading enum.
        :param shape: The shape of a card as a Shape enum.
        """

        if number < 1 or number > 3:
            raise ValueError('The number can only be between 1 and 3, '
                             'instead it was {}'.format(number))

        if color not in Color:
            raise ValueError('Unexpected color {}'.format(color))

        if shading not in Shading:
            raise ValueError('Unexpected shading {}'.format(shading))

        if shape not in Shape:
            raise ValueError('Unexpected shape {}'.format(shape))

        self.number = number
        self.color = color
        self.shading = shading
        self.shape = shape
        pass

    def findLastCardInSet(self, other):
        """
        Returns the card to a complete a set given two other cards.

        :param other: The other card.

        :returns: The SetCard that completes the set.
        """

        if self.number == other.number:
            last_number = self.number
        else:
            # If they are all different, the three values must sum to 6.
            last_number = 6 - self.number - other.number

        if self.color == other.color:
            last_color = self.color
        else:
            last_color = Color(6 - self.color.value - other.color.value)

        if self.shading == other.shading:
            last_shading = self.shading
        else:
            last_shading = Shading(6 - self.shading.value
                                   - other.shading.value)

        if self.shape == other.shape:
            last_shape = self.shape
        else:
            last_shape = Shape(6 - self.shape.value - other.shape.value)

        return SetCard(last_number, last_color, last_shading, last_shape)

    @property
    def _card_num(self):
        """
        A property to uniquely identify this card from all the others.

        Because each property has 3 possible values, they are encoded in
        base 3.
        """
        return (self.number
                + self.color.value * 3
                + self.shading.value * 9
                + self.shape.value * 27)

    def __eq__(self, other):
        """
        Overload equality testing to ensure all the properties match.
        """
        return self._card_num == other._card_num

    def __lt__(self, other):
        """
        Overload less than to provide a consistent card ordering when sorting.
        """
        return self._card_num < other._card_num

    def __str__(self):
        """
        More readable string representation of object.
        """

        return ('SetCard: Number: {}, Color: {}, Shape: {}, Shading: {}'
                .format(self.number, self.color.name, self.shape.name,
                        self.shading.name))

    def __repr__(self):
        """
        More readable representation of object in console.
        """
        return str(self)

    def __hash__(self):
        """
        Necessary to be used in sets/dictionaries.
        """
        return self._card_num


def findAllSets(cards):
    """
    Returns all the sets contained in the cards in play.

    :param cards: A list of SetCards in play.

    :returns: A list of all sets of 3 cards that form a set.
    """
    sets = []
    for (card1, card2) in itertools.combinations(cards, 2):
        card3 = card1.findLastCardInSet(card2)
        if card3 in cards:
            new_set = set((card1, card2, card3))
            if new_set not in sets:
                sets.append(new_set)

    return sets


class SetGame:
    """
    Runs a simple game of set.
    """

    def __init__(self, num_cards_in_play=12):
        """
        Creates a new object.

        :param num_card_in_play: The number of cards to deal out at a time.
        """
        self.deck = self._generateDeck()
        self.num_cards_in_play = num_cards_in_play

        self.cards_in_play = []
        for ix in range(self.num_cards_in_play):
            self.dealCard()

    def dealCard(self):
        """
        Deals a card from the deck onto the board.

        :returns: True if a card was dealt.
        """
        if len(self.deck) > 0:
            self.cards_in_play.append(self.deck.pop())
            return True
        else:
            return False

    def removeCard(self, card):
        """
        Removes a card from the playing area and deals a new card if necessary.

        :param card: The card to remove.
        """
        self.cards_in_play.remove(card)

        if len(self.cards_in_play) < self.num_cards_in_play:
            self.dealCard()

    def _generateDeck(self):
        """
        Generates a new deck of cards.
        """
        deck = []
        for num in [1, 2, 3]:
            for color in Color:
                for shape in Shape:
                    for shading in Shading:
                        deck.append(SetCard(num, color, shading, shape))

        random.shuffle(deck)
        return deck

    def isASet(self, cards):
        """
        Returns True if the cards form a set.
        """
        cards = list(cards)
        if not (cards[0].number == cards[1].number == cards[2].number
                or cards[0].number != cards[1].number != cards[2].number):
            return False

        if not (cards[0].color == cards[1].color == cards[2].color
                or cards[0].color != cards[1].color != cards[2].color):
            return False

        if not (cards[0].shape == cards[1].shape == cards[2].shape
                or cards[0].shape != cards[1].shape != cards[2].shape):
            return False

        if not (cards[0].shading == cards[1].shading == cards[2].shading
                or cards[0].shading != cards[1].shading != cards[2].shading):
            return False

        return True


if __name__ == '__main__':
    game = SetGame(num_cards_in_play=12)
    while True:
        possible_sets = findAllSets(game.cards_in_play)
        for s in possible_sets:
            if not game.isASet(s):
                print('Bad set: {}'.format(s))
        print('Found {} sets with {} cards!'.format(len(possible_sets),
                                                    len(game.cards_in_play)))
        if len(possible_sets) > 1:
            for c in possible_sets[0]:
                game.removeCard(c)
        else:
            was_dealt = game.dealCard()
            if not was_dealt:
                break
