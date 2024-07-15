import random

def play(bet_amount):
    # Simple roulette logic
    result = random.uniform(-bet_amount, bet_amount * 1.5)
    return round(result, 2)