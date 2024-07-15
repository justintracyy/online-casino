import random

def play(bet_amount):
    # Simple slot machine logic
    result = random.uniform(-bet_amount, bet_amount * 2)
    return round(result, 2)