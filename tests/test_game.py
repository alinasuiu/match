from unittest import TestCase
from unittest.mock import patch
from game import Game, Card, UnauthorisedNumberOfDecksException, UnknownMatchTypeException

class Test(TestCase):

    def test_negative_number_of_cards(self):
        # checks that the constructor throws an exception if we have a negative number in the place of numberOfDecks
        with self.assertRaises(UnauthorisedNumberOfDecksException):
            game = Game(-1,"values")

    def test_float_number_of_cards(self):
        # checks that the constructor throws an exception if we have a float number in the place of numberOfDecks
        with self.assertRaises(UnauthorisedNumberOfDecksException):
            game = Game(1.5,"values")

    def test_string_number_of_cards(self):
        # checks that the constructor throws an exception if we have a string in the place of numberOfDecks
        with self.assertRaises(UnauthorisedNumberOfDecksException):
            game = Game("1.5","values")

    def test_negative_unknown_match(self):
        # checks that the constructor throws an exception if we have an unknown match type
        with self.assertRaises(UnknownMatchTypeException):
            game = Game(1,"value")

    def test_pick_a_card(self):
        # tests that the card that was picked is in the deck
        game = Game(1,"values")
        result = game.pickCard()
        self.assertIn(result,game.deck)

    @patch("game.Game.pickCard")
    def test_pick_a_card_from_deck(self, pickcard):
        # tests that after all cards of a type are taken out of the deck, you can't pick the same card again
        pickcard.return_value = Card("king","hearts")
        game = Game(2, "values")
        game.addToPile(Card("king","hearts"))
        game.addToPile(Card("king","hearts"))
        self.assertEqual(game.pile, 2)
        card = game.pickCard()
        game.addToPile(card)
        self.assertEqual(game.pile, 2)

    def test_add_to_pile(self):
        # checks that a card has been added to the pile
        game = Game(1, "values")
        game.addToPile(Card("king","hearts"))
        self.assertEqual(game.pile,1)

    def test_pick_player(self):
        # tests that the random number generator has picked a valid player
        game = Game(1, "values")
        player = game.pickPlayer(["A","B"])
        self.assertIn(player,["A","B"])

    def test_take_pile(self):
        # checks that after a player wins a round, the pile gets added to their score
        game = Game(1,"values")
        game.addToPile(Card("king","hearts"))
        game.addToPile(Card("3","clubs"))
        game.takePile("A")
        self.assertEqual(game.scores,[2,0])

    def test_match(self):
        # checks that the match functions work as expected
        game = Game(1,"suits")
        cards = [Card("king","hearts"),Card("3","hearts")]
        self.assertEqual(game.match(cards),True)
        game = Game(1, "values")
        cards = [Card("king", "hearts"), Card("3", "hearts")]
        self.assertEqual(game.match(cards), False)
        game = Game(1, "values")
        cards = [Card("king", "hearts"), Card("king", "clubs")]
        self.assertEqual(game.match(cards), True)
        game = Game(1, "values")
        cards = [Card("king", "hearts"), Card("queen", "clubs")]
        self.assertEqual(game.match(cards), False)

    def test_get_cards_for_players(self):
        # checks that valid cards were picked for each player and the correct number of cards were added to the pile
        game = Game(1, "values")
        cards = game.getCardsForPlayers()
        self.assertNotIn(cards[0],game.deck)
        self.assertNotIn(cards[1], game.deck)
        self.assertIn(cards[0].suit,game.suits)
        self.assertIn(cards[1].suit, game.suits)
        self.assertIn(cards[0].value, game.values)
        self.assertIn(cards[1].value, game.values)
        self.assertEquals(game.pile, 2)

    def test_compare_cards_and_pick_player(self):
        # checks that, given two cards that have been picked out, the right score gets calculated
        cards = [Card("ace","hearts"),Card("ace","clubs")]
        game = Game(1, "values")
        game.pile = 2
        game.compareCardsAndPickWinner(cards)
        self.assertEquals(set(game.scores),set([2,0]))

    @patch("game.Game.pickPlayer")
    def test_play_draw(self, player):
        # checks that after a number of rounds have been played, the draw condition can be achieved
        player.return_value = "A"
        game = Game(2, "values")
        game.deck = {
            Card("ace","spades"): 2,
        }
        game.pile = 0
        game.scores =[50,52]
        self.assertEquals(game.play(),"DRAW")

    @patch("game.Game.pickPlayer")
    def test_play_A_wins(self, player):
        # checks that if player A wins, the right output gets returned
        player.return_value = "A"
        game = Game(2, "values")
        game.deck = {
            Card("ace", "spades"): 2,
        }
        game.pile = 0
        game.scores = [52, 48]
        self.assertEquals(game.play(), "A")

    @patch("game.Game.pickPlayer")
    def test_play_B_wins(self, player):
        # checks that if player B wins, then the right output gets returned
        player.return_value = "B"
        game = Game(2, "suits")
        game.deck = {
            Card("ace", "spades"): 2,
            Card("2", "spades"): 2,
        }
        game.pile = 0
        game.scores = [48, 48]
        self.assertEquals(game.play(), "B")
