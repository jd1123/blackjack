from bjcore import MultiDeck, Hand, DealerHand, BankRoll
import os, sys

class Game(object):
	config = {'shuffle_threshold': 0.35, 
				'Ace' : 14, 
				'Face' : [11,12,13],
				'default_wager': 25,
				'starting_bankroll' : 500,
				'num_decks': 6,
				'blackjack_payout': 1.5,
				'insurance_payout': 2,
				'save_bankroll': True
				}
	
	def __init__(self):
		self.game_state = 'Welcome'
		self.game_deck = MultiDeck(Game.config['num_decks'])
		self.player_hand = Hand()
		self.dealer_hand = DealerHand()
		self.run_flag = True
		self.play_hand_container = []
		
		if Game.config['save_bankroll']:
			try:
				with open('bankroll.txt' , 'r') as file:
					old_balance = int(file.read())
				
				if old_balance <= 0:
					old_balance = 500
				
				self.bank_roll = BankRoll(old_balance)
			
			except (IOError, ValueError):
				self.bank_roll = BankRoll(Game.config['starting_bankroll'])
			
		
		self.run_game()
	
	#show the count of the deck		
	def print_count(self):
		print 'The count is ' + str(self.game_deck.deck_count()) + '....\n'
	
	def clear_screen(self):
		if os.name == 'posix':
			os.system('clear')
		
		elif os.name == 'nt':
			os.system('cls')
	
	#check to see if all hands are busts
	def all_hands_busted(self):
		b = 1
		
		for h in self.play_hand_container:
			b*=h.busted*1
		return b
	
	#break to keep the game pace
	def game_pause(self):
		print 'Press Enter to continue.'
		player_input = raw_input()
	
	#Show the hands from the perspective of a player
	#if the reveal flag is set to true, it will show the 
	#dealer's down card
	def show_state(self , msg='', reveal=False):
		self.clear_screen()
		print msg + '\n'
		i=len(self.play_hand_container) - 1
		j = 0
		
		for h in self.play_hand_container:	
			s = h.show_hand()
			if not(h.hand_active):
				s = s + '  *'
			if (i):
				s = 'Hand ' + str(j) + ': ' + s
			else:
				s = 'Your Hand: ' + s 
			print s
			print
			j+=1
			
		dh = ''
		
		if reveal:
			dh = self.dealer_hand.reveal_hand()
		
		else:
			dh = self.dealer_hand.show_hand()
		
		print 'Dealer Hand: ' + dh
		print
	
	#Main Welcome Screen
	def welcome_screen(self):
		self.clear_screen()
		print "======================="
		print "Welcome to BlackJack!"
		print "======================="
		print 
		print "=======================\n"
		print 'Some info:\n'
		print 'Cards are shown as (K of D)'
		print 'The first letter or number is the card value, the second is the suit\n'
		print 'D = Diamonds, S = Spades, C = Clubs, H = Hearts\n'
		print
		print 'Additional Rules:'
		print '* Insurance pays ' +str(Game.config['insurance_payout']) + ':1, and is for half the size of your bet'
		print '* Dealer stands on soft 17s'
		print '* There are no surrenders'
		print "=======================\n"
		self.game_pause()
	
	#Game over screen	
	def game_over_screen(self):
		self.game_pause()
		self.run_flag = False
		self.clear_screen()
		print "=======================\n"
		print "Game Over"
		print "Thank you for playing!\n"
		print "=======================\n"
		if Game.config['save_bankroll']:
			try:
				with open('bankroll.txt', 'w') as file:
					file.write(str(self.bank_roll.balance))
			except (IOError):
				pass
			
	
	#Take the input from a bet and do some logic	
	def bet_input(self):
		self.clear_screen()
		bet_ok = False
		self.bank_roll.print_bank_roll()
		
		while not(bet_ok):	
			bet_input = raw_input('What is your bet? (Default is ' + str(Game.config['default_wager']) + '): ')
			
			try:
				bet_int = int(bet_input)
				
				if bet_int > self.bank_roll.balance:
					print 'You do not have that much cash!\nPlease try again.'
				elif bet_int == 0:
					print 'You must bet something'
				elif bet_int < 0:
					print "Why, aren't you clever. Please try again"
					
				else:
					self.player_hand.wager = bet_int
					bet_ok = True
				
			except ValueError:
				
				if bet_input.upper() == 'Q':
					print 'Quitting game...'
					self.game_state = 'GameOver'
					return None
				
				elif bet_input == '*':
					self.print_count()
				
				else:
					self.player_hand.wager = Game.config['default_wager']
					bet_ok = True
			
		
		self.clear_screen()
		print 'You have bet ' + str(self.player_hand.wager),
		return self.player_hand.wager
	
	#Deal the hand in the right order
	def start_hand(self):	
		
		if (self.game_deck.percent_cards_remaining() < Game.config['shuffle_threshold']):
			print '\nReshuffling deck...\n'
			self.game_pause()
			self.game_deck.shuffle()
			
		
		insurance = False
		
		self.play_hand_container = []
		
		self.player_hand.add_card_to_hand(self.game_deck.draw_card())
		self.dealer_hand.add_card_to_hand(self.game_deck.draw_card())
		self.player_hand.add_card_to_hand(self.game_deck.draw_card())
		self.dealer_hand.add_card_to_hand(self.game_deck.draw_card())
		
		''' THIS IS FOR DEBUG TO CHECK SPLITS'' 
		c = self.game_deck.draw_card()
		self.player_hand.add_card_to_hand(c)
		self.player_hand.add_card_to_hand(c)
		##############################'''
		
		'''THIS IS FOR DEBUG TO TEST INSURANCE''
		self.player_hand.add_card_to_hand([('S',9)])
		self.player_hand.add_card_to_hand([('S',13)])
		self.dealer_hand.add_card_to_hand([('D',6)])
		self.dealer_hand.add_card_to_hand([('D', 14)])
		#################'''
		
		self.play_hand_container.append(self.player_hand)
		self.show_state()
		
		insurance_amount = 0
		
		if self.dealer_hand.last_card()[1]==Game.config['Ace']:
			print 'Would you like insurance? (Y/n)'	
			flag = True
			
			while flag:
				player_input = raw_input().upper()
				
				if player_input == 'Y':
					insurance_amount = int(self.player_hand.wager/2)
					if self.bank_roll.has_enough(self.player_hand.wager + insurance_amount):
						insurance = True
						print 'You have taken insurance for ' + str(insurance_amount)
						flag = False
						self.game_pause()
						self.clear_screen()
					
					else:
						print 'You do not have enough for insurance\n'
						flag = False
						insurance = False
						
				elif player_input == 'N':
					print 'You have declined insurance\n'
					self.game_pause()
					self.clear_screen()
					flag = False
					self.show_state(msg = 'You have bet ' + str(self.player_hand.wager))
				
				else:
					print 'You entered something incorrectly. Please type (Y) for yes or (N) for no.'
		
		if self.dealer_hand.reveal_value()==21:
			
			if (self.player_hand.hand_value() == 21):
				print 'Push'
				if insurance:
					insurance_payout = Game.config['insurance_payout']*insurance_amount
					self.bank_roll.inc(insurance_payout)
					print 'But you had insurance! You win ' + str(insurance_payout) + '.\n'
				
				else:
					print '**** No Money Exchanged ****'
				
				self.game_pause()
				return False
			
			else:
				self.show_state('Dealer has 21', reveal=True)
				print 'Dealer has 21, you lose ' + str(self.player_hand.wager)
				self.bank_roll.dec(self.player_hand.wager)
				if insurance:
					insurance_payout = Game.config['insurance_payout']*insurance_amount
					self.bank_roll.inc(insurance_payout)
					print 'But you had insurance! You win ' + str(insurance_payout)
				
				self.game_pause()
				return False
		else:
			
			if self.player_hand.hand_value()==21:
				print 'BLACKJACK!'
				print 'You win ' + str(int(self.player_hand.wager*Game.config['blackjack_payout']))
				self.bank_roll.inc(int(self.player_hand.wager*Game.config['blackjack_payout']))
				if insurance:
					self.bank_roll.dec(insurance_amount)
					print 'Your bankroll has been reduced by ' + str(insurance_amount) + ' for insurance'
				
				self.game_pause()
				return False
			
			else:
				if insurance:
					self.bank_roll.dec(insurance_amount)
					print 'The dealer does not have blackjack.'
					print 'Your bankroll has been reduced by the insurance wager of ' + str(insurance_amount)
					print 'You now have: ' + str(self.bank_roll.balance)
					self.game_pause()
					self.clear_screen()
					self.show_state(msg = 'You have bet ' + str(self.player_hand.wager) )
				
				return True
	
	#This is the dealer logic for after the player makes all decisions
	#Stand on soft 17s
	def dealer_logic(self):
		dealer_go = True
		self.game_pause()
		
		while(dealer_go):
			
			if self.dealer_hand.reveal_value() < 17:
				print 'Dealer Hits!'
				print 'Dealer Draws: ' + self.dealer_hand.hit(self.game_deck)
				print 'Dealer Hand: ' + self.dealer_hand.reveal_hand() + '\n'
			
			elif self.dealer_hand.reveal_value() > 21:
				self.clear_screen()
				self.show_state(msg='Dealer Busts!', reveal=True)
				
				dealer_go=False
				return self.dealer_hand.reveal_hand()
			
			else:
				self.clear_screen()
				self.show_state('Dealer Stands!', reveal=True) 
				dealer_go=False
				return self.dealer_hand.reveal_hand()
			
			self.game_pause()
			
	#Evaluate the hand(s) after the dealer has played
	def evaluate_hand(self, plrhand, dealer_done = True, msg = None):
		if msg:
			print msg
		plr = plrhand.hand_value()
		dlr = self.dealer_hand.reveal_value()
			
		if plr > 21:
			print 'Player Busts!\n'
			plrhand.busted = True
			
			if dealer_done:	
				print '**** Player loses ' + str(plrhand.wager) + '.\n'
				self.bank_roll.dec(plrhand.wager)
				return False
			
			return False
			
		if dealer_done:	
			
			if(dlr>21):
				print 'Dealer Busts!'
				print '**** Player wins ' + str(plrhand.wager) + '. ****\n'
				self.bank_roll.inc(plrhand.wager)
				return False
			
			elif (dlr==plr):
				print 'Push\n'
				print '**** No Money Exchanged. ****'
				return False
			
			elif (dlr>plr):
				print 'Dealer Wins :('
				print '**** Player loses ' + str(plrhand.wager) + '. ****\n'
				self.bank_roll.dec(plrhand.wager)
				return False
			
			elif (plr>dlr):
				print '**** Player wins: ' + str(plrhand.wager) + '. ****\n'
				self.bank_roll.inc(plrhand.wager)
				return False
				
		return True
	
	#Get player input for each hand
	def player_logic(self, player_go):
		hand_index=0
		
		for h in self.play_hand_container:
			
			while h.hand_active:		
				
				if len(self.play_hand_container)>1:
					print 'Active Hand: ' + str(hand_index)
				
				print 'What would you like to do?'
				player_input = raw_input('(H) hit, (S) stand, (D) double down, (I) split, or (Q) quit : ').upper()
				
				if player_input == 'H':
					self.clear_screen()
					h.hit(self.game_deck)
					self.show_state(msg = 'You Hit!')
					print 'You drew: ' + self.player_hand.last_card_formatted()
					h.hand_active = self.evaluate_hand(h, dealer_done = False)
				
				elif player_input == 'S':
					h.hand_active = False
					self.clear_screen()
					self.show_state('You Stand!', reveal = False)

				elif player_input == 'D':
					if h.card_count() > 2:
						print '\nYou cannot double down. \n'
					else:
						if h.wager*2 <= self.bank_roll.balance:	
							self.clear_screen()
							
							h.wager*=2
							h.hit(self.game_deck)
							self.show_state('DOUBLE DOWN!', reveal = False)
							print 'You drew: ' + self.player_hand.last_card_formatted() + '\n'
							self.evaluate_hand(h, dealer_done = False)
							h.hand_active = False
							self.game_pause()
						
						else:
							print 'You do not have that much cash, and so you cannot double down'
							print 'Please try again.\n'
					
				elif player_input == 'Q':
					print 'Quitting game...'
					self.game_state = 'GameOver'
					h.hand_active = False
					return False
				
				elif player_input == '*':
					self.print_count()
				
				elif player_input == 'I':
					can_split = self.player_hand.can_split()
					
					if (can_split and self.bank_roll.has_enough(h.wager*(len(self.play_hand_container)+1))):
						print 'You can split'
						new_hand = Hand()
						new_hand.add_card_to_hand(h.pop_card())
						new_hand.add_card_to_hand(self.game_deck.draw_card())
						new_hand.wager = h.wager
						h.add_card_to_hand(self.game_deck.draw_card())
						self.play_hand_container.append(new_hand)
						self.show_state('You Split!', reveal = False)

					else:
						print 'You cannot split'
						 
				
				else:
					print 'That input is not recognized. Try again.'

			hand_index+=1
		return True
	
	#This is the main game logic
	#Logical order is:
	#1) set up the hand
	#2) get player decisions
	#3) have the dealer play
	#4) evaluate the hand and change the bankroll
	def main_game_logic(self):
		
		self.player_hand.clr_hand()
		self.dealer_hand.clr_hand()
		player_go = True
		
		bet = None
		if self.bank_roll.has_enough(1):
			bet = self.bet_input()
			if (bet == None):
				player_go = False
			else:
				player_go = self.start_hand()
		else:
			print 'You are all out of cash!'
			player_go = False
			self.game_state = 'GameOver'
			
		if (player_go):
			player_done = self.player_logic(player_go)
			if (player_done):
				if not(self.all_hands_busted()):
					self.show_state(msg = "Dealer's Turn", reveal=True)
					self.dealer_logic()
				
				self.game_pause()
				self.clear_screen()
				
				for h in self.play_hand_container:
					msg=''
					if len(self.play_hand_container) > 1:
						msg = 'Hand ' + str(self.play_hand_container.index(h)) + ' result:'
					self.evaluate_hand(h, dealer_done = True, msg=msg)
					self.game_pause()
		
	#The main loop
	def run_game(self):
		while (self.run_flag):
			
			if self.game_state == 'Welcome':
				self.welcome_screen()
				self.game_state = "MainState"
			
			elif self.game_state == 'MainState':
				self.main_game_logic()
			
			elif self.game_state == 'GameOver':
				self.game_over_screen()

def main():
	game = Game()

if __name__ == '__main__':
	status = main()
	sys.exit(status)
