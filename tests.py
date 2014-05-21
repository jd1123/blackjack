from bjcore import MultiDeck, Hand
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

class HandTest(unittest.TestCase):
    
    def setUp(self):
        self.my_deck = MultiDeck(4)
        self.hand = Hand()
    
    def test_addingcards(self):
        card = self.my_deck.draw_card()
        self.hand.add_card_to_hand(card)
        self.assertEqual(len(self.hand.cards_in_hand),1, 'There is not one and only one card in the hand after adding one')
        self.assertTrue(card==self.hand.pop_card(), 'pop_card did not return the same object as the last card in hand')
        self.assertEqual(len(self.hand.cards_in_hand), 0, 'pop_card did not remove the card in hand')
        
def main():
    unittest.main()
    
if __name__=='__main__':
    status = main()
    sys.exit(status)