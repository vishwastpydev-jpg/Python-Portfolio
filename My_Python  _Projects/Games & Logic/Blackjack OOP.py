


## Milestone Project 2

# Importing libraries -- used for shuffling cards
import random

# Boolean type to know whether play is in hand
playing = False

# Amount for buy-in
chip_pool = 100
print('Your buy-in amount is:', chip_pool)

bet = 1

restart_phrase = "Press d to deal the cards again, or press q to quit."

# Hearts, Diamonds, Clubs, Spades
suits = ('H','D','S','C')

# Possible Card Ranks
ranking = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')

# Point Val Dict (Dual existence of Ace is defined later)
card_val = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

# Creating Card Class

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.suit + self.rank

    def grab_suit(self):
        return self.suit

    def grab_rank(self):
        # NOTE: Removed 'rank' argument from definition
        return self.rank

    def draw(self):
        print(self.suit + self.rank)

# Creating Hand Class
# Gives dual existence to Ace

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0

        # Aces can be 1 0r 11 as defined below
        self.ace = False

    def __str__(self):
        '''Return a string of current hand composition'''
        hand_comp = ""

        # List Comprehension
        for card in self.cards:
            card_name = card.__str__()
            hand_comp += " " + card_name

        return 'The hand has %s' %hand_comp

    def card_add(self,card):
        '''Add another card to the hand'''
        self.cards.append(card)

        # Checking for Aces
        if card.rank == 'A':
            self.ace = True
        self.value += card_val[card.rank]

    def calc_val(self):
        '''Calculating value of hand, making aces = 1 if they don't bust the hand'''

        # Checks for an ace and if value is less than 12 (i.e. <= 11)
        if (self.ace == True and self.value < 12):
            return self.value + 10
        else:
            return self.value

    def draw(self, hidden):
        if hidden == True and playing == True:
            # Don't show first hidden card
            starting_card = 1
            print("XX", end=" ") # Display 'XX' for the hidden card
        else:
            starting_card = 0
        
        # Draw remaining cards in the hand
        for x in range(starting_card, len(self.cards)):
            self.cards[x].draw()


# Creating Class Deck

class Deck:

    def __init__(self):
        '''Creating a deck in order'''
        self.deck = []
        for suit in suits:
            for rank in ranking:
                self.deck.append(Card(suit,rank))

    def shuffle(self):
        '''Shuffles the deck, using python's built-in random library'''
        random.shuffle(self.deck)

    def deal(self):
        '''Grabbing the first item in the deck'''
        single_card = self.deck.pop()
        return single_card

    def __str__(self):
        # NOTE: This implementation was incorrect. A Deck object doesn't have 'cards'. 
        # A simple string representation is better for a deck object.
        return "A deck of " + str(len(self.deck)) + " cards."

# End of Classes

# First Bet

def make_bet():
    '''Ask the player for the bet amount and '''

    global bet, chip_pool
    bet = 0

    print ('\nWhat amount of chips would you like to bet? (Please enter whole integer) ')

    # While loop to keep asking for the bet
    while bet == 0:
        try:
            # Using input() for Python 3
            bet_comp = int(input())
        except ValueError:
            print("Please enter a valid number.")
            continue # Go back to the start of the while loop

        # Check to make sure the bet is within the remaining amount of chips left
        if bet_comp >= 1 and bet_comp <= chip_pool:
            bet = bet_comp
        else:
            print ("Invalid bet, you only have " + str(chip_pool) + " remaining")

def deal_cards():
    '''This function deals out cards and sets up round'''

    # Set up all global variables
    global result, playing, deck, player_hand, dealer_hand, chip_pool, bet

    # Check for bankruptcy before dealing
    if chip_pool <= 0:
        print("You're out of chips! Game Over.")
        game_exit()
        return

    # Creating a deck
    deck = Deck()

    # Shuffle it
    deck.shuffle()

    # Set up the bet
    make_bet()

    # Set up both player and dealer hands
    player_hand = Hand()
    dealer_hand = Hand()

    # Deal out initial cards (Player, Dealer, Player, Dealer)
    player_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())
    player_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())

    result = "Hit or Stand? Press h for hit or s for stand: "

    # Original code had a check here for playing==True that seems wrong 
    # (Fold, Sorry). Removed it as a new deal means a new, fresh hand.

    # Set up to know currently playing hand
    playing = True
    game_step()


# Hit Function

def hit():
    '''Implementing the hit button'''

    global playing, chip_pool, deck, player_hand, dealer_hand, result, bet

    # If hand is in play add card
    if playing:
        # Check if the player has already busted based on the current hand value
        if player_hand.calc_val() <= 21:
            player_hand.card_add(deck.deal())

        print ("Player hand is %s" %player_hand)

        if player_hand.calc_val() > 21:
            result = 'Busted! ' + restart_phrase

            chip_pool -= bet
            playing = False

    else:
        result = "Sorry, can't hit. " + restart_phrase

    game_step()

# Stand Function

def stand():
    global playing, chip_pool, deck, player_hand, dealer_hand, result, bet

    '''This function plays the dealers hand, since stand was chosen'''

    if playing == False:
        # If the player hasn't busted, standing when not 'playing' (i.e. already finished the round) 
        # is probably an error state. This path only runs if something went wrong.
        if player_hand.calc_val() > 0:
             # The result should be set by the previous logic (bust/win/etc)
             pass 

    # Going through all other possible options
    else:
        playing = False # Player stands, no more player action

        # Soft 17 Rule (Dealer hits until >= 17)
        while dealer_hand.calc_val() < 17:
            print("\nDealer Hits...")
            dealer_hand.card_add(deck.deal())

        # Dealer Busts
        if dealer_hand.calc_val() > 21:
            result = 'Dealer busts! You win! ' + restart_phrase
            chip_pool += bet

        # Player has better hand than dealer
        elif dealer_hand.calc_val() < player_hand.calc_val():
            result = 'You beat the dealer, you win! ' + restart_phrase
            chip_pool += bet

        # Push
        # NOTE: Fixed the call of calc_val on dealer_hand in the original code
        elif dealer_hand.calc_val() == player_hand.calc_val(): 
            result = 'Tied up, push!' + restart_phrase

        # Dealer beats player
        else:
            result = 'Dealer Wins! ' + restart_phrase
            chip_pool -= bet

    game_step()

# Function to print results and ask user for next step

def game_step():
    '''Function to print game step/status on output'''

    # Display Player Hand
    print ("\n" + "-"*30)
    print ('Player Hand is:', end=' ')
    player_hand.draw(hidden = False)
    print ('Player hand total is:', player_hand.calc_val())

    # Display Dealer Hand
    print ('\nDealer Hand is:', end=' ')
    dealer_hand.draw(hidden = True)

    # If game round is over
    if playing == False:
        # Display the hidden card and the total
        print(" revealing the hidden card...")
        print('Dealer Hand is:', end=' ')
        dealer_hand.cards[0].draw() # Display the first card
        for x in range(1, len(dealer_hand.cards)):
             dealer_hand.cards[x].draw()
        
        print( " --- for a total of " + str(dealer_hand.calc_val()))
        print ("Chip Total: " +str(chip_pool))
        print ("-"*30)

    # Otherwise, don't know the second card yet
    else:
        print (" (with another card hidden upside down)")

    # Print result of hit or stand
    print ('\n' + result)

    player_input()


# Function to exit the game

def game_exit():
    print ('Thanks for playing!')
    exit()

# Function to read user input

def player_input():
    '''Read user input, lower case it just to be safe'''

    # Using input() for Python 3
    plin = input().lower()

    if plin == 'h':
        hit()
    elif plin == 's':
        stand()
    elif plin == 'd':
        deal_cards()
    elif plin == 'q':
        game_exit()
    else:
        print ("Invalid Input. Enter h, s, d, or q: ")
        player_input()

# Intro to game

def intro():
    statement = '''Welcome to BlackJack! Get as close to 21 as you can without getting over! 
Dealer hits until she reaches 17. Aces count as 1 or 11. Card output goes a letter followed by a number of face notation. '''

    print (statement)
    print ('')

# Playing the Game

'''The following code will initiate the game!'''

# Print the intro
intro()

# Create a Deck (Will be re-created in deal_cards, but here for completeness)
deck = Deck()

# Create player and dealer hands (Will be re-created in deal_cards)
player_hand = Hand()
dealer_hand = Hand()

# Deal out the cards and start the game!
deal_cards()