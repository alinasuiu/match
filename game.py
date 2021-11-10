from random import randrange
from dataclasses import dataclass
from typing import List
from logging import debug


class UnauthorisedNumberOfDecksException(Exception):
    pass


class UnknownMatchTypeException(Exception):
    pass

@dataclass(frozen=True, eq=True)
class Card:
    value: str
    suit: str

class Game():
    def __init__(self, numberOfDecks: int, matchType: str):
        if not isinstance(numberOfDecks,int) or numberOfDecks <= 0:
            raise UnauthorisedNumberOfDecksException
        self.players = ["A", "B"]
        self.values = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        self.suits = ["clubs", "diamonds", "hearts", "spades"]
        self.matchTypes = {"suits": self.matchSuits, "values": self.matchValues,
                           "Both suits and values": self.matchSuitsAndValues}
        self.pile = 0
        if matchType in self.matchTypes.keys():
            self.matchType = matchType
        else:
            raise UnknownMatchTypeException()
        self.deck = {}
        # a dictionary where:
        #  - the keys are the card type
        #  - the value is the number of occurrences of each type of card that we start with
        for value in self.values:
            for suit in self.suits:
                self.deck[Card(value,suit)] = numberOfDecks
        self.scores = [0] * len(self.players)

    def matchSuits(self, cards: List[Card]) -> bool:
        suits = [card.suit for card in cards]
        return all(x == suits[0] for x in suits)

    def matchValues(self, cards: List[Card]) -> bool:
        values = [card.value for card in cards]
        return all(x == values[0] for x in values)

    def matchSuitsAndValues(self, cards: List[Card]) -> bool:
        return self.matchSuits(cards) and self.matchValues(cards)

    def addToPile(self, card:Card):
        if card in self.deck.keys():
            if self.deck[card] == 1:
                # removes the card if the one picked is the last one of its kind
                self.deck.pop(card)
                # increases the size of the pile
                self.pile += 1
            else:
                # decreases the number of cards of that kind that are available
                self.deck[card] -= 1
                # increases the size of the pile
                self.pile += 1

    def pickCard(self)->Card:
        # picks a card from the ones that are still in the deck
        cardsAvailable = list(self.deck.keys())
        card = cardsAvailable[randrange(len(cardsAvailable))]
        return card

    def pickPlayer(self, players)->str:
        # picks a player from the list of players
        return players[randrange(len(players))]

    def takePile(self, player:str):
        # adds the number of cards in the pile to the player who won that round
        self.scores[self.players.index(player)] += self.pile
        # resets the pile
        self.pile = 0

    def match(self, cards:List[Card]):
        # sees if the cards picket match
        return self.matchTypes[self.matchType](cards)

    def getCardsForPlayers(self) -> List[Card]:
        # picks a card and adds it to the pile for each player
        cards = []
        for i in range(0, len(self.players)):
            # picks a card for each player
            card = self.pickCard()
            cards.append(card)
            # adds the card to the pile
            self.addToPile(card)
        return cards

    def compareCardsAndPickWinner(self, cards:List[Card]):
        # sees if the cards picked match and assigns a winner
        if self.match(cards):
            # picks the first player to say "match"
            player = self.pickPlayer(self.players)
            # increases the score of said player by the amount of the pile
            self.takePile(player)

    def play(self) -> str:
        # plays the game while there are still cards left in the big deck
        while self.deck:
            cards = self.getCardsForPlayers()
            # checks if the two cards picked in this round match by the criteria chosen and assigns a winner of the round
            self.compareCardsAndPickWinner(cards)
        # returns the winner
        return self.players[self.scores.index(max(self.scores))] if not all(x == self.scores[0] for x in self.scores) else "DRAW"

