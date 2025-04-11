import random

# Define card colors and values
COLORS = ["Red", "Yellow", "Green", "Blue"]
VALUES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw Two"]
WILD_CARDS = ["Wild", "Wild Draw Four"]

# Generate the deck
def create_deck():
    deck = []
    for color in COLORS:
        for value in VALUES:
            deck.append((color, value))  # Each number/action card appears twice except 0
            if value != "0":
                deck.append((color, value))
    for _ in range(4):  # 4 wild cards
        deck.append(("Wild", "Wild"))
        deck.append(("Wild", "Wild Draw Four"))
    random.shuffle(deck)
    return deck

# Initialize players
def deal_cards(deck, num_players):
    players = {i: [deck.pop() for _ in range(7)] for i in range(num_players)}
    return players

# Check if a move is valid
def is_valid_move(card, top_card):
    return (card[0] == top_card[0] or  # Same color
            card[1] == top_card[1] or  # Same number/action
            card[0] == "Wild")         # Wild card

# Main game loop
def play_uno():
    num_players = int(input("Enter number of players: "))
    deck = create_deck()
    players = deal_cards(deck, num_players)
    top_card = deck.pop()  # Start with a card

    turn = 0
    direction = 1  # 1 for normal, -1 for reverse

    while True:
        print(f"\nTop Card: {top_card[0]} {top_card[1]}")
        player = turn % num_players
        print(f"Player {player + 1}'s turn. Your cards:")
        for i, card in enumerate(players[player]):
            print(f"{i}: {card[0]} {card[1]}")

        move = input("Choose card number to play or 'd' to draw: ")
        if move == "d":
            new_card = deck.pop()
            players[player].append(new_card)
            print(f"Drew a card: {new_card[0]} {new_card[1]}")
        else:
            move = int(move)
            chosen_card = players[player][move]
            if is_valid_move(chosen_card, top_card):
                top_card = chosen_card
                players[player].pop(move)

                if chosen_card[1] == "Reverse":
                    direction *= -1
                elif chosen_card[1] == "Skip":
                    turn += direction  # Skip next player
                elif chosen_card[1] == "Draw Two":
                    next_player = (turn + direction) % num_players
                    players[next_player].extend([deck.pop(), deck.pop()])
                elif chosen_card[0] == "Wild":
                    new_color = input("Choose color (Red, Yellow, Green, Blue): ")
                    top_card = (new_color, chosen_card[1])
                    if chosen_card[1] == "Wild Draw Four":
                        next_player = (turn + direction) % num_players
                        players[next_player].extend([deck.pop(), deck.pop(), deck.pop(), deck.pop()])

                if not players[player]:
                    print(f"Player {player + 1} wins!")
                    break
            else:
                print("Invalid move! Try again.")
                continue  # Don't change turn on invalid move

        turn += direction

play_uno()