from bjcore import MultiDeck, Hand, DealerHand, BankRoll
import os, sys

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


game_state = 'Welcome'
game_deck = MultiDeck(config['num_decks'])
player_hand = Hand()
dealer_hand = DealerHand()
run_flag = True
play_hand_container = []
bank_roll = BankRoll()

#show the count of the deck        
def print_count():
    print 'The count is ' + str(game_deck.deck_count()) + '....\n'

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    
    elif os.name == 'nt':
        os.system('cls')

#check to see if all hands are busts
def all_hands_busted():
    b = 1
    
    for h in play_hand_container:
        b*=h.busted*1
    return b

#break to keep the game pace
def game_pause():
    print 'Press Enter to continue.'
    player_input = raw_input()

#Show the hands from the perspective of a player
#if the reveal flag is set to true, it will show the 
#dealer's down card
def show_state(msg='', reveal=False):
    clear_screen()
    print msg + '\n'
    i=len(play_hand_container) - 1
    j = 0
    
    for h in play_hand_container:    
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
        dh = dealer_hand.reveal_hand()
    
    else:
        dh = dealer_hand.show_hand()
    
    print 'Dealer Hand: ' + dh
    print

#Main Welcome Screen
def welcome_screen():
    clear_screen()
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
    print '* Insurance pays ' +str(config['insurance_payout']) + ':1, and is for half the size of your bet'
    print '* Dealer stands on soft 17s'
    print '* There are no surrenders'
    print "=======================\n"
    game_pause()

#Game over screen    
def game_over_screen():
    global run_flag
    
    game_pause()
    run_flag = False
    clear_screen()
    print "=======================\n"
    print "Game Over"
    print "Thank you for playing!\n"
    print "=======================\n"
    if config['save_bankroll']:
        try:
            with open('bankroll.txt', 'w') as file:
                file.write(str(bank_roll.balance))
        except (IOError):
            pass
        

#Take the input from a bet and do some logic    
def bet_input():
    global bank_roll
    global game_state
    global game_deck
    global player_hand
    global dealer_hand
    global run_flag
    global play_hand_container
    global bank_roll

    clear_screen()
    bet_ok = False
    bank_roll.print_bank_roll()
    
    while not(bet_ok):    
        bet_input = raw_input('What is your bet? (Default is ' + str(config['default_wager']) + '): ')
        
        try:
            bet_int = int(bet_input)
            
            if bet_int > bank_roll.balance:
                print 'You do not have that much cash!\nPlease try again.'
            elif bet_int == 0:
                print 'You must bet something'
            elif bet_int < 0:
                print "Why, aren't you clever. Please try again"
                
            else:
                player_hand.wager = bet_int
                bet_ok = True
            
        except ValueError:
            
            if bet_input.upper() == 'Q':
                print 'Quitting game...'
                game_state = 'GameOver'
                return None
            
            elif bet_input == '*':
                print_count()
            
            else:
                player_hand.wager = config['default_wager']
                bet_ok = True
        
    
    clear_screen()
    print 'You have bet ' + str(player_hand.wager),
    return player_hand.wager

#Deal the hand in the right order
def start_hand():    
    global bank_roll
    global game_state
    global game_deck
    global player_hand
    global dealer_hand
    global run_flag
    global play_hand_container
    global bank_roll

    
    if (game_deck.percent_cards_remaining() < config['shuffle_threshold']):
        print '\nReshuffling deck...\n'
        game_pause()
        game_deck.shuffle()
        
    
    insurance = False
    
    play_hand_container = []
    
    player_hand.add_card_to_hand(game_deck.draw_card())
    dealer_hand.add_card_to_hand(game_deck.draw_card())
    player_hand.add_card_to_hand(game_deck.draw_card())
    dealer_hand.add_card_to_hand(game_deck.draw_card())
    
    ''' THIS IS FOR DEBUG TO CHECK SPLITS'' 
    c = game_deck.draw_card()
    player_hand.add_card_to_hand(c)
    player_hand.add_card_to_hand(c)
    ##############################'''
    
    '''THIS IS FOR DEBUG TO TEST INSURANCE''
    player_hand.add_card_to_hand([('S',9)])
    player_hand.add_card_to_hand([('S',13)])
    dealer_hand.add_card_to_hand([('D',6)])
    dealer_hand.add_card_to_hand([('D', 14)])
    #################'''
    
    play_hand_container.append(player_hand)
    show_state()
    
    insurance_amount = 0
    
    if dealer_hand.last_card()[1]==config['Ace']:
        print 'Would you like insurance? (Y/n)'    
        flag = True
        
        while flag:
            player_input = raw_input().upper()
            
            if player_input == 'Y':
                insurance_amount = int(player_hand.wager/2)
                if bank_roll.has_enough(player_hand.wager + insurance_amount):
                    insurance = True
                    print 'You have taken insurance for ' + str(insurance_amount)
                    flag = False
                    game_pause()
                    clear_screen()
                
                else:
                    print 'You do not have enough for insurance\n'
                    flag = False
                    insurance = False
                    
            elif player_input == 'N':
                print 'You have declined insurance\n'
                game_pause()
                clear_screen()
                flag = False
                show_state(msg = 'You have bet ' + str(player_hand.wager))
            
            else:
                print 'You entered something incorrectly. Please type (Y) for yes or (N) for no.'
    
    if dealer_hand.reveal_value()==21:
        
        if (player_hand.hand_value() == 21):
            print 'Push'
            if insurance:
                insurance_payout = config['insurance_payout']*insurance_amount
                bank_roll.inc(insurance_payout)
                print 'But you had insurance! You win ' + str(insurance_payout) + '.\n'
            
            else:
                print '**** No Money Exchanged ****'
            
            game_pause()
            return False
        
        else:
            show_state('Dealer has 21', reveal=True)
            print 'Dealer has 21, you lose ' + str(player_hand.wager)
            bank_roll.dec(player_hand.wager)
            if insurance:
                insurance_payout = config['insurance_payout']*insurance_amount
                bank_roll.inc(insurance_payout)
                print 'But you had insurance! You win ' + str(insurance_payout)
            
            game_pause()
            return False
    else:
        
        if player_hand.hand_value()==21:
            print 'BLACKJACK!'
            print 'You win ' + str(int(player_hand.wager*config['blackjack_payout']))
            bank_roll.inc(int(player_hand.wager*config['blackjack_payout']))
            if insurance:
                bank_roll.dec(insurance_amount)
                print 'Your bankroll has been reduced by ' + str(insurance_amount) + ' for insurance'
            
            game_pause()
            return False
        
        else:
            if insurance:
                bank_roll.dec(insurance_amount)
                print 'The dealer does not have blackjack.'
                print 'Your bankroll has been reduced by the insurance wager of ' + str(insurance_amount)
                print 'You now have: ' + str(bank_roll.balance)
                game_pause()
                clear_screen()
                show_state(msg = 'You have bet ' + str(player_hand.wager) )
            
            return True

#This is the dealer logic for after the player makes all decisions
#Stand on soft 17s
def dealer_logic():
    global bank_roll
    global game_state
    global game_deck
    global player_hand
    global dealer_hand
    global run_flag
    global play_hand_container
    global bank_roll

    
    dealer_go = True
    game_pause()
    
    while(dealer_go):
        
        if dealer_hand.reveal_value() < 17:
            print 'Dealer Hits!'
            print 'Dealer Draws: ' + dealer_hand.hit(game_deck)
            print 'Dealer Hand: ' + dealer_hand.reveal_hand() + '\n'
        
        elif dealer_hand.reveal_value() > 21:
            clear_screen()
            show_state(msg='Dealer Busts!', reveal=True)
            
            dealer_go=False
            return dealer_hand.reveal_hand()
        
        else:
            clear_screen()
            show_state('Dealer Stands!', reveal=True) 
            dealer_go=False
            return dealer_hand.reveal_hand()
        
        game_pause()
        
#Evaluate the hand(s) after the dealer has played
def evaluate_hand(plrhand, dealer_done = True, msg = None):
    global bank_roll
    global game_state
    global game_deck
    global player_hand
    global dealer_hand
    global run_flag
    global play_hand_container
    global bank_roll

    
    if msg:
        print msg
    plr = plrhand.hand_value()
    dlr = dealer_hand.reveal_value()
        
    if plr > 21:
        print 'Player Busts!\n'
        plrhand.busted = True
        
        if dealer_done:    
            print '**** Player loses ' + str(plrhand.wager) + '.\n'
            bank_roll.dec(plrhand.wager)
            return False
        
        return False
        
    if dealer_done:    
        
        if(dlr>21):
            print 'Dealer Busts!'
            print '**** Player wins ' + str(plrhand.wager) + '. ****\n'
            bank_roll.inc(plrhand.wager)
            return False
        
        elif (dlr==plr):
            print 'Push\n'
            print '**** No Money Exchanged. ****'
            return False
        
        elif (dlr>plr):
            print 'Dealer Wins :('
            print '**** Player loses ' + str(plrhand.wager) + '. ****\n'
            bank_roll.dec(plrhand.wager)
            return False
        
        elif (plr>dlr):
            print '**** Player wins: ' + str(plrhand.wager) + '. ****\n'
            bank_roll.inc(plrhand.wager)
            return False
            
    return True

#Get player input for each hand
def player_logic(player_go):
    global bank_roll
    global game_state
    global game_deck
    global player_hand
    global dealer_hand
    global run_flag
    global play_hand_container
    global bank_roll

    
    hand_index=0
    
    for h in play_hand_container:
        
        while h.hand_active:        
            
            if len(play_hand_container)>1:
                print 'Active Hand: ' + str(hand_index)
            
            print 'What would you like to do?'
            player_input = raw_input('(H) hit, (S) stand, (D) double down, (I) split, or (Q) quit : ').upper()
            
            if player_input == 'H':
                clear_screen()
                h.hit(game_deck)
                show_state(msg = 'You Hit!')
                print 'You drew: ' + player_hand.last_card_formatted()
                h.hand_active = evaluate_hand(h, dealer_done = False)
            
            elif player_input == 'S':
                h.hand_active = False
                clear_screen()
                show_state('You Stand!', reveal = False)

            elif player_input == 'D':
                if h.card_count() > 2:
                    print '\nYou cannot double down. \n'
                else:
                    if h.wager*2 <= bank_roll.balance:    
                        clear_screen()
                        
                        h.wager*=2
                        h.hit(game_deck)
                        show_state('DOUBLE DOWN!', reveal = False)
                        print 'You drew: ' + player_hand.last_card_formatted() + '\n'
                        evaluate_hand(h, dealer_done = False)
                        h.hand_active = False
                        game_pause()
                    
                    else:
                        print 'You do not have that much cash, and so you cannot double down'
                        print 'Please try again.\n'
                
            elif player_input == 'Q':
                print 'Quitting game...'
                game_state = 'GameOver'
                h.hand_active = False
                return False
            
            elif player_input == '*':
                print_count()
            
            elif player_input == 'I':
                can_split = player_hand.can_split()
                
                if (can_split and bank_roll.has_enough(h.wager*(len(play_hand_container)+1))):
                    print 'You can split'
                    new_hand = Hand()
                    new_hand.add_card_to_hand(h.pop_card())
                    new_hand.add_card_to_hand(game_deck.draw_card())
                    new_hand.wager = h.wager
                    h.add_card_to_hand(game_deck.draw_card())
                    play_hand_container.append(new_hand)
                    show_state('You Split!', reveal = False)

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
def main_game_logic():
    global bank_roll
    global game_state
    global game_deck
    global player_hand
    global dealer_hand
    global run_flag
    global play_hand_container
    global bank_roll

    player_hand.clr_hand()
    dealer_hand.clr_hand()
    player_go = True
    
    bet = None
    if bank_roll.has_enough(1):
        bet = bet_input()
        if (bet == None):
            player_go = False
        else:
            player_go = start_hand()
    else:
        print 'You are all out of cash!'
        player_go = False
        game_state = 'GameOver'
        
    if (player_go):
        player_done = player_logic(player_go)
        if (player_done):
            if not(all_hands_busted()):
                show_state(msg = "Dealer's Turn", reveal=True)
                dealer_logic()
            
            game_pause()
            clear_screen()
            
            for h in play_hand_container:
                msg=''
                if len(play_hand_container) > 1:
                    msg = 'Hand ' + str(play_hand_container.index(h)) + ' result:'
                evaluate_hand(h, dealer_done = True, msg=msg)
                game_pause()
    
#The main loop
def run_game():
    global bank_roll
    global game_state
    global game_deck
    global player_hand
    global dealer_hand
    global run_flag
    global play_hand_container
    global bank_roll

    
    if config['save_bankroll']:
        try:
            with open('bankroll.txt' , 'r') as file:
                old_balance = int(file.read())
            
            if old_balance <= 0:
                old_balance = 500
            
            bank_roll = BankRoll(old_balance)
        
        except (IOError, ValueError):
            bank_roll = BankRoll(config['starting_bankroll'])

    while (run_flag):
        
        if game_state == 'Welcome':
            welcome_screen()
            game_state = "MainState"
        
        elif game_state == 'MainState':
            main_game_logic()
        
        elif game_state == 'GameOver':
            game_over_screen()

def main():
    run_game()

if __name__ == '__main__':
    status = main()
    sys.exit(status)
