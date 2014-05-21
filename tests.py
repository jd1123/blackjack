from bjcore import MultiDeck
import unittest
import sys

class MultiDeckTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_reshuffle(self):
        multi_deck = MultiDeck(4)
        c = multi_deck.draw_card()
        multi_deck.shuffle()
        d_pile = multi_deck.discard_pile
        self.assertEqual(len(multi_deck.deck), 4*52, 'The amount of cards does not equal decks * 52' )
        self.assertTrue((c in multi_deck.deck), 'The drawn card is not in the reshuffled deck')
        self.assertEqual(d_pile, [], 'The discard pile is not empty on reshuffle')    
    
def main():
    unittest.main()
    
if __name__=='__main__':
    status = main()
    sys.exit(status)