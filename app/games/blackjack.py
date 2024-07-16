import random
import uuid

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def to_dict(self):
        return {"suit": self.suit, "value": self.value}

class Deck:
    def __init__(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
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

def simulate_blackjack(player_balance, bet_amount):
    game_id = str(uuid.uuid4())
    deck = Deck()
    player_hand = [deck.draw(), deck.draw()]
    dealer_hand = [deck.draw(), deck.draw()]
    
    player_value = calculate_hand_value(player_hand)  # Initialize player_value here
    dealer_value = calculate_hand_value(dealer_hand)
    
    status = "in_progress"
    available_actions = ["hit", "stand", "double_down"]
    last_action = "initial_deal"
    outcome = None
    payout = 0  # Initialize payout

    # Simulate player's turn
    while player_value < 17:  # Simple strategy: hit on 16 or less
        player_hand.append(deck.draw())
        player_value = calculate_hand_value(player_hand)
        last_action = "hit"
        if player_value > 21:
            status = "completed"
            outcome = "Player busts! Dealer wins."
            payout = -bet_amount  # Player loses the bet
            player_balance += payout
            break

    # Simulate dealer's turn if player hasn't busted
    if status != "completed":
        while dealer_value < 17:
            dealer_hand.append(deck.draw())
            dealer_value = calculate_hand_value(dealer_hand)
        
        status = "completed"
        if dealer_value > 21:
            outcome = "Dealer busts! Player wins."
            payout = bet_amount  # Player wins the bet
        elif dealer_value > player_value:
            outcome = "Dealer wins!"
            payout = -bet_amount  # Player loses the bet
        elif player_value > dealer_value:
            outcome = "Player wins!"
            payout = bet_amount  # Player wins the bet
        else:
            outcome = "It's a tie!"
            payout = 0  # Player gets their bet back
        
        player_balance += payout

    return {
        "gameId": game_id,
        "status": status,
        "playerHand": [card.to_dict() for card in player_hand],
        "playerHandValue": player_value,
        "dealerHand": [dealer_hand[0].to_dict(), {"suit": "hidden", "value": "hidden"}] if status == "in_progress" else [card.to_dict() for card in dealer_hand],
        "dealerHandValue": calculate_hand_value([dealer_hand[0]]) if status == "in_progress" else dealer_value,
        "currentBet": bet_amount,
        "playerBalance": player_balance,
        "availableActions": available_actions if status == "in_progress" else [],
        "lastAction": last_action,
        "outcome": outcome,
        "payout": payout
    }