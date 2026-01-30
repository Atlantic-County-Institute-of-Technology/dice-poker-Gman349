# imports
import inquirer3
from dice import *
from collections import Counter
import os

# variables
dice = Dice()
def_dice_rolls = 3

# dice photos
topstr = "┏━━━━━━━━━━━┓"
btmstr = "┗━━━━━━━━━━━┛"
oned = ["┃           ┃",
        "┃     ●     ┃",
        "┃           ┃"]

twod = ["┃ ●         ┃",
        "┃           ┃",
        "┃         ● ┃"]

threed = ["┃ ●         ┃",
          "┃     ●     ┃",
          "┃         ● ┃"]

fourd = ["┃ ●       ● ┃",
         "┃           ┃",
         "┃ ●       ● ┃"]

fived = ["┃ ●       ● ┃",
         "┃     ●     ┃",
         "┃ ●       ● ┃"]

sixd = ["┃ ●       ● ┃",
        "┃ ●       ● ┃",
        "┃ ●       ● ┃"]

facelist = [oned, twod, threed, fourd, fived, sixd]  # list the dice together


def show(keepl, final):
    # create each row to compile dice
    top = ""
    topcenter = ""
    center = ""
    bottomcenter = ""
    bottom = ""
    if not final:
        dicelist = dice.roll_dice(keepl)
    else:
        dicelist = keepl
    for i in dicelist:  # for each dice, compile each row of dice
        face = facelist[i - 1]
        top = top + " " + topstr  # add each top section of the dice
        # for each dice in the list, add the middle sections corresponding to the dice face number
        topcenter = topcenter + " " + str(face[0])
        center = center + " " + str(face[1])
        bottomcenter = bottomcenter + " " + str(face[2])
        bottom = bottom + " " + btmstr  # add each bottom section of the dice
    if not final:
        print(f"{top}\n{topcenter}\n{center}\n{bottomcenter}\n{bottom}")  # print each row of the dice
        return dicelist
    else:
        return f"{top}\n{topcenter}\n{center}\n{bottomcenter}\n{bottom}"


def keep(keepl, items_to_add):  # for each new dice to keep, append dice number to corresponding keep list
    for i in items_to_add:
        keepl.append(i)


def get_score(hand1, hand2, comp_or_prsn):
    hand_ranks = ["Five of a Kind", "Four of a Kind", "Full House", "Straight", "Three of a Kind", "Two Pair",
                  "One Pair", "Bust"]  # each rank in order

    def evaluate_hand(hand):
        if len(hand) != 5:
            return "Bust", (0, 0, 0, 0, 0)  # If hand is incomplete, treat as Bust with low tiebreakers

        sorted_hand = sorted(hand, reverse=True)  # sort in descending order
        counts = Counter(hand)
        count_values = sorted(counts.values(), reverse=True)  # the amount of each number there are
        unique_values = sorted(counts.keys(), reverse=True)  # what the numbers of the dice are without repetitions

        is_straight = (len(counts) == 5) and (sorted_hand[0] - sorted_hand[4] == 4)  # Check for Straight
        if count_values[0] == 5:  # checks for five of a kind
            rank = "Five of a Kind"
            tiebreak = (list(counts.keys())[0],)
        elif count_values[0] == 4:  # checks for four of a kind
            rank = "Four of a Kind"
            four_val = max(k for k, v in counts.items() if v == 4)  # generates value for 4 of a kind
            single = next(k for k, v in counts.items() if v == 1)  # generates value for standalone 5th dice
            tiebreak = (four_val, single)
        elif count_values == [3, 2]:  # checks for full house
            rank = "Full House"
            three_val = next(k for k, v in counts.items() if v == 3)  # generates value for 3 pair
            pair_val = next(k for k, v in counts.items() if v == 2)  # generates value for 2 pair
            tiebreak = (three_val, pair_val)
        elif is_straight:  # pulls down check for straight
            rank = "Straight"
            tiebreak = (sorted_hand[0],)  # generates value for highest dice value
        elif count_values[0] == 3:
            rank = "Three of a Kind"  # checks for three of a kind
            three_val = next(k for k, v in counts.items() if v == 3)  # generates value for 3 pair
            singles = sorted([k for k, v in counts.items() if v == 1], reverse=True)  # creates list of standalone dice
            tiebreak = (three_val, singles[0], singles[1])  # generates value of 3 pair and standalone dice
        elif count_values == [2, 2, 1]:  # checks for two of a kind
            rank = "Two Pair"
            pairs = sorted([k for k, v in counts.items() if v == 2], reverse=True)  # creates list of the pairs
            single = next(k for k, v in counts.items() if v == 1)  # creates list of single dice
            tiebreak = (pairs[0], pairs[1], single)  # generates value for pairs and single dice
        elif count_values[0] == 2:  # checks for pair (two of a kind)
            rank = "One Pair"
            pair_val = next(k for k, v in counts.items() if v == 2)  # generates value for pair
            singles = sorted([k for k, v in counts.items() if v == 1], reverse=True)  # creates list of standalone dice
            tiebreak = (pair_val, singles[0], singles[1], singles[2])  # generates value of pair and standalone dice
        else:  # if no others, it's a bust
            rank = "Bust"
            tiebreak = tuple(sorted_hand)  # generates bust value

        return rank, tiebreak

    # evaluates each hand
    rank1, tie1 = evaluate_hand(hand1)
    rank2, tie2 = evaluate_hand(hand2)

    name = "Player 2" if comp_or_prsn == 1 else "Computer"  # assigns name to player 2/computer

    print("FINAL HANDS:\n"  # prints final hands
          f"Player 1:\n{show(hand1, True)} ({rank1})\n"
          f"{name}:\n{show(hand2, True)} ({rank2})\n")
    # gets value of ranks
    rank_idx1 = hand_ranks.index(rank1)
    rank_idx2 = hand_ranks.index(rank2)
    # compares value of ranks
    if rank_idx1 < rank_idx2:
        print("Player 1 wins!")
    elif rank_idx1 > rank_idx2:
        print(f"{name} wins!")
    else:  # if tiebreaker, run this instead
        # Compare tiebreaker values
        if tie1 > tie2:
            print("Player 1 wins! (tiebreaker)")
        elif tie1 < tie2:
            print(f"{name} wins! (tiebreaker)")
        else:
            print("It's a tie!")


def player_turn(dice_rolls, keepl):
    dlist = show(keepl, False)  # displays dice to player and generates number list
    dice_rolls = dice_rolls - 1  # subtract roll counter
    if dice_rolls == 0:
        keepqa = dlist[len(keepl):]
        keep(keepl, keepqa)
    else:
        play = [
            inquirer3.List("play", message="What would you like to do?", choices=["Keep Dice", "End Turn"])
        ]
        answer = inquirer3.prompt(play)

        if answer["play"] == "Keep Dice":
            newly_rolled_dice = dlist[len(keepl):]
            if newly_rolled_dice:
                keepquestion = [
                    inquirer3.Checkbox("menu",
                                       message="Which dice would you like to keep? (Space to select, enter to confirm)",
                                       choices=newly_rolled_dice)
                ]
                keepqa = inquirer3.prompt(keepquestion)
                print(f"Keeping {keepqa['menu']}")
                keep(keepl, keepqa["menu"])
            else:
                print("No unkept dice to keep!")

    return dice_rolls


def computer_turn(dice_rolls, keepl):
    dlist = show(keepl, False)
    newly_rolled = dlist[len(keepl):]
    dice_rolls = dice_rolls - 1

    if not newly_rolled:
        print("No dice to roll, hand is full.")
        return dice_rolls

    current_counts = Counter(keepl)
    new_counts = Counter(newly_rolled)
    to_keep = []

    if current_counts:
        # Prefer the highest value with max frequency
        max_freq = max(current_counts.values())
        candidates = [k for k, v in current_counts.items() if v == max_freq]
        max_freq_val = max(candidates)

        # Keep all that match the target
        to_keep = [d for d in newly_rolled if d == max_freq_val]

    if not to_keep:  # No match or no current
        if max(new_counts.values()) >= 2:
            # Keep all dice in groups of 2 or more
            to_keep = [d for d in newly_rolled if new_counts[d] >= 2]
        else:
            if dice_rolls > 0:
                to_keep = []
            else:
                to_keep = newly_rolled

    # If last roll and hand not full, add the highest singles to fill
    new_hand_size = len(keepl) + len(to_keep)
    if dice_rolls == 0 and new_hand_size < 5:
        not_kept = [d for d in newly_rolled if d not in to_keep]
        # Sort descending
        singles = sorted(not_kept, reverse=True)
        needed = 5 - new_hand_size
        additional = singles[:needed]
        to_keep += additional

    print(f"Computer keeping: {to_keep}")
    keep(keepl, to_keep)
    return dice_rolls


def player_vs_computer():
    p1keep = []
    ckeep = []
    p1dice_rolls = int(def_dice_rolls)
    cdice_rolls = int(def_dice_rolls)
    playing = True

    while playing:
        if p1dice_rolls > 0:
            print(f"\n--- PLAYER 1 TURN ({p1dice_rolls - 1} rolls left) ---")
        p1dice_rolls = player_turn(p1dice_rolls, p1keep)
        if cdice_rolls > 0:
            print(f"\n--- COMPUTER TURN ({cdice_rolls - 1} rolls left) ---")
        cdice_rolls = computer_turn(cdice_rolls, ckeep)
        print("\n-------------------------")
        if p1dice_rolls == 0 and cdice_rolls == 0:
            playing = False
            print("Game Over!")
            get_score(p1keep, ckeep, 0)


def player_vs_player():
    p1keep = []
    p2keep = []
    p1dice_rolls = int(def_dice_rolls)
    p2dice_rolls = int(def_dice_rolls)
    playing = True

    while playing:
        if p1dice_rolls > 0:
            print(f"\n--- PLAYER 1 TURN ({p1dice_rolls} rolls left) ---")
        p1dice_rolls = player_turn(p1dice_rolls, p1keep)
        if p2dice_rolls > 0:
            print(f"\n--- PLAYER 2 TURN ({p2dice_rolls} rolls left) ---")
        p2dice_rolls = player_turn(p2dice_rolls, p2keep)
        print("\n-------------------------")
        if p1dice_rolls == 0 and p2dice_rolls == 0:
            playing = False
            print("Game Over!")
            get_score(p1keep, p2keep, 1)


def main():
    menu = [
        inquirer3.List("menu",
                       message="What would you like to do? (Enter to choose)",
                       choices=["1 vs. Computer", "1 vs. 1", "Exit"])
    ]
    menu_answers = inquirer3.prompt(menu)
    os.system('cls' if os.name == "nt" else 'clear')
    if menu_answers["menu"] == "1 vs. Computer":
        player_vs_computer()
    elif menu_answers["menu"] == "Exit":
        exit()
    else:
        player_vs_player()


# test

while __name__ == '__main__':
    main()
