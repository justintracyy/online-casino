import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card.value in ['J', 'Q', 'K']:
            value += 10
        elif card.value == 'A':
            aces += 1
        else:
            value += int(card.value)
    
    for _ in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1
    
    return value

def play_blackjack(bet_amount):
    deck = Deck()
    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    # Player's turn
    while player_value < 21:
        if random.choice([True, False]):  # Simulating player's decision to hit or stand
            player_hand.append(deck.draw())
            player_value = calculate_hand_value(player_hand)
        else:
            break

    # Dealer's turn
    while dealer_value < 17:
        dealer_hand.append(deck.draw())
        dealer_value = calculate_hand_value(dealer_hand)

    # Determine winner
    if player_value > 21:
        return -bet_amount, "Player busts! Dealer wins."
    elif dealer_value > 21:
        return bet_amount, "Dealer busts! Player wins."
    elif player_value > dealer_value:
        return bet_amount, "Player wins!"
    elif dealer_value > player_value:
        return -bet_amount, "Dealer wins!"
    else:
        return 0, "It's a tie!"