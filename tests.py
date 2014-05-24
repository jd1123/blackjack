from bjcore import MultiDeck, Hand, BankRoll
import unittest
import sys

# Testing the multideck function
class MultiDeckTest(unittest.TestCase):
    
    def setUp(self):
        self.multi_deck = MultiDeck(4)
    
    def test_init(self):
        num_decks = 4
        deck = MultiDeck(num_decks)
        self.assertEqual(len(deck.deck), num_decks*52, 'The MultiDeck does not contain the correct number of cards')
        self.assertEqual(deck.numdecks, num_decks, 'The MultiDeck.numdecks attribute is not equal to the argument')
    
    def test_draw(self):
        pass
    
    def test_reshuffle(self):
        multi_deck = MultiDeck(4)
        c = multi_deck.draw_card()
        multi_deck.shuffle()
        d_pile = multi_deck.discard_pile
        self.assertEqual(len(multi_deck.deck), 4*52, 'The amount of cards does not equal decks * 52' )
        self.assertTrue((c in multi_deck.deck), 'The drawn card is not in the reshuffled deck')
        self.assertEqual(d_pile, [], 'The discard pile is not empty on reshuffle')    

# Will test the hand object for functionality
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
    
    def test_clr_hand(self):
        card = self.my_deck.draw_card()
        self.hand.add_card_to_hand(card)
        self.hand.clr_hand()
        self.assertEqual(self.hand.cards_in_hand, [], 'There are cards in the hand after clearing')
        self.assertTrue(self.hand.hand_active, 'Hand is not active after clearing')
        self.assertFalse(self.hand.busted, 'Busted flag is not false after clearing')
        self.assertEqual(self.hand.soft, 0, 'Soft counter is not 0 after clearing')
    
    def test_hit(self):
        self.my_deck.shuffle()
        self.hand.clr_hand()

class BankRollTest(unittest.TestCase):
    
    def setUp(self):
        self.roll = BankRoll()
    
    def test_init(self):
        roll = BankRoll(400)
        self.assertEqual(roll.balance, 400, "The bankroll does not init to the proper value when an argument is passed to the constructor")
        
    def test_inc_dec(self):
        self.roll.inc(100)
        self.assertEqual(self.roll.balance, 600, "The bankroll object does not inc correctly")
        self.roll.dec(100)
        self.assertEqual(self.roll.balance, 500, "The bankroll object does not dec correctly")
        
    def test_has_enough(self):
        self.assertTrue(self.roll.has_enough(2), "Bankroll object has_enough does not work when the balance is higher than argument")
        self.assertTrue(self.roll.has_enough(-1), "Bankroll.has_enough() does not work for negative numbers")
        self.assertFalse(self.roll.has_enough(1000), "Bankroll.has_enough does not work when balance is smaller than argument" )

class DealerHandTest(unittest.TestCase):
    
    def setUp(self):
        self.dh = DealerHand()
        
        
def main():
    unittest.main()
    
if __name__=='__main__':
    status = main()
    sys.exit(status)