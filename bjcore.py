#
# This is the core for the blackjack game.
# It has a host of objects for the flow of gameplay
#

from random import randrange

class Deck(object):
    def __init__(self):
        self.deck=[]
        suites = ['D', 'H', 'S', 'C']
        cards = range(2,15)
        i=0
        for s in suites:
            for r in cards:
                self.deck.append((s,r))
                i+=1

    def cards(self):
        return self.deck
#
# Many decks object
#
class MultiDeck(object):
    def __init__(self, numdecks):
        self.numdecks = numdecks 
        self.deck = []
        self.discard_pile = []      
        self.shuffle() 
                
    def cards_remaining(self):
        return len(self.deck)
    
    def percent_cards_remaining(self):
        return float(self.cards_remaining())/float((self.numdecks*52))
    
    def draw_card(self, count=1):
        drawn_card = []
        for i in range(0,count):            
            rand_index = randrange(0,len(self.deck))
            drawn_card.append(self.deck[rand_index])
            self.discard_pile.append(self.deck[rand_index])
            del self.deck[rand_index]
        return drawn_card

    def shuffle(self):
        self.deck = []
        for i in range(0,self.numdecks):
            self.deck+=Deck().cards()
            
    def deck_count(self):
        hc = lambda x: x>9*1
        lc = lambda x: x<7*1
        highcards = sum([hc(c[1]) for c in self.discard_pile])
        lowcards = sum([lc(c[1]) for c in self.discard_pile])
        return lowcards-highcards

class Hand(object):
    def __init__(self):
        self.cards_in_hand = []
        self.soft = 0
        self.hand_active = True
        self.busted = False
        self.wager = 5
    
    def add_card_to_hand(self, card):
        if card[0][1] == 14:
            self.soft += 1
        self.cards_in_hand += card
        
    def hit(self, deck):
        card = deck.draw_card()
        self.add_card_to_hand(card)
        return self.format_card(card[0])

    def hand_value(self):        
        self.v = 0        
        if self.cards_in_hand:        
            for c in self.cards_in_hand:
                if 14 > c[1] > 10:
                    self.v+=10
                elif c[1] == 14:
                    self.v += 11
                else:
                    self.v+=c[1]
            
            if self.v > 21:
                i=0
                while (self.v>21 and i< self.soft):
                    self.v-=10
                    i+=1
            
            return self.v            
                
        else:
            return 0
    
    def format_card(self, card):
        
        cardDict = {11:'J', 12:'Q', 13:'K', 14:'A'}
        if card[1]>10:
            return '(' + str(cardDict[card[1]])+ ' of ' + str(card[0]) + ')'
        else:
            return '('+str(card[1])+' of '+str(card[0])+')'
    
    def show_hand(self):
        return ' '.join([self.format_card(c) for c in self.cards_in_hand])+':'+str(self.hand_value())
    
    def clr_hand(self):
        self.cards_in_hand = []
        self.soft = 0
        self.hand_active = True
        self.busted = False
    
    def last_card(self):
        return  self.cards_in_hand[-1]
    
    def last_card_formatted(self):
        return  self.format_card(self.cards_in_hand[-1])
    
    def pop_card(self):
        try: 
            index = len(self.cards_in_hand) - 1 
            card = self.cards_in_hand[index]
            self.cards_in_hand.remove(card)
            return [card]
        except IndexError:
            return []
    
    def card_count(self):
        return len(self.cards_in_hand)
    
    def card_value(self, card):
        if 2 <= card[0][1] <= 9:
            return card[0][1]
        elif 10<=card[0][1]<=13:
            return 10
        elif card[0][1] == 14:
            return 11
    
    def can_split(self):
        if self.card_count() == 2:
            return self.card_value([self.cards_in_hand[0]]) ==  self.card_value([self.cards_in_hand[1]])
        else:
            return False
        
class DealerHand(Hand):
    def __init__(self):
        Hand.__init__(self)
        
    def hand_value(self):
        v = int(self.last_card()[1])
        if (14>v>10):
            return 10
        elif (v==14):
            return 11
        else:
            return v     
     
    def show_hand(self):
        return '(*, *) '+' '.join([self.format_card(c) for c in self.cards_in_hand[1:]])+':'+str(self.hand_value())
    
    def reveal_hand(self):
        return ' '.join([self.format_card(c) for c in self.cards_in_hand])+':'+str(Hand.hand_value(self))
    
    def reveal_value(self):
        return Hand.hand_value(self)

class BankRoll(object):
    def __init__(self, balance = 500):
        self.balance = balance
    
    def inc(self, amount):
        self.balance+=amount
    
    def dec(self, amount):
        self.balance-=amount
        
    def print_bank_roll(self):
        print 'You currently have: ' + str(self.balance)
        
    def has_enough(self, bet):
        if bet>self.balance:
            return False
        else:
            return True
