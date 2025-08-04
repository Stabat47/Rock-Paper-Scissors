# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

import random
from collections import Counter

# Global state variables - ensure these are outside the player function
my_history = []
opponent_history_global = []
round_count = 0
beats = {"R": "P", "P": "S", "S": "R"}
# Define the reverse for convenience if needed (what beats X)
what_beats_me = {"R": "P", "P": "S", "S": "R"} 

ROUNDS_PER_OPPONENT = 1000

def player(prev_play, opponent_history=[]): # opponent_history parameter is ignored in favor of global
    global round_count, my_history, opponent_history_global, beats, what_beats_me

    # --- Game Start/Reset Logic ---
    if prev_play == "" and round_count == 0:
        my_history.clear()
        opponent_history_global.clear()
        round_count = 0
    elif prev_play:
        opponent_history_global.append(prev_play)
    
    round_count += 1

    current_opponent_round = (round_count - 1) % ROUNDS_PER_OPPONENT + 1

    if current_opponent_round == 1 and round_count > 1: # Reset for new opponent
        my_history.clear()
        opponent_history_global.clear()

    move = random.choice(["R", "P", "S"]) # Default move

    # --- Strategy per Opponent ---

    # Quincy (Rounds 1-1000)
    if round_count <= ROUNDS_PER_OPPONENT:
        quincy_pattern = ["R", "R", "P", "P", "S"]
        predicted_quincy_move = quincy_pattern[(current_opponent_round - 1) % len(quincy_pattern)]
        move = beats[predicted_quincy_move]

    # Mrugesh (Rounds 1001-2000)
    elif round_count <= ROUNDS_PER_OPPONENT * 2:
    
        if current_opponent_round == 1:
            move = "P" 
        elif prev_play:
            
            r = random.random()
            if r < 0.70: 
                move = beats[prev_play]
            elif r < 0.90: 
                move = random.choice(["R", "P", "S"])
            else: 
                move = prev_play
        else:
            
            move = random.choice(["R", "P", "S"])

    # Kris (Rounds 2001-3000)
    elif round_count <= ROUNDS_PER_OPPONENT * 3:
        if len(my_history) > 0:
            kris_predicted_play = beats[my_history[-1]]
            move = beats[kris_predicted_play]
        else:
            move = random.choice(["R", "P", "S"])

    # Abbey (Rounds 3001-4000)
    else: # This block handles Abbey
        play_order = {} 
        if len(opponent_history_global) >= 3:
            for i in range(len(opponent_history_global) - 2):
                sequence = "".join(opponent_history_global[i:i+2])
                next_move = opponent_history_global[i+2]
                if sequence not in play_order:
                    play_order[sequence] = {"R": 0, "P": 0, "S": 0}
                play_order[sequence][next_move] += 1
            
            last_two_opp = "".join(opponent_history_global[-2:])
            if last_two_opp in play_order:
                possible_next_moves = play_order[last_two_opp]
                if any(possible_next_moves.values()):
                    predicted_abbey_next = max(possible_next_moves, key=possible_next_moves.get)
                    move = beats[predicted_abbey_next]
                else:
                    if len(opponent_history_global) > 5:
                        most_frequent_opp_move = Counter(opponent_history_global).most_common(1)[0][0]
                        move = beats[most_frequent_opp_move]
                    else:
                        move = random.choice(["R", "P", "S"])
            else:
                if len(opponent_history_global) > 5:
                    most_frequent_opp_move = Counter(opponent_history_global).most_common(1)[0][0]
                    move = beats[most_frequent_opp_move]
                else:
                    move = random.choice(["R", "P", "S"])
        else:
            move = random.choice(["R", "P", "S"])

    my_history.append(move)
    return move
    