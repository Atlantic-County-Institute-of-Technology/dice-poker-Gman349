# imports
import inquirer3
from dice import *
from collections import Counter

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


def show(keepl):
    top = ""
    topcenter = ""
    center = ""
    bottomcenter = ""
    bottom = ""
    dicelist = dice.roll_dice(keepl)
    for i in dicelist:
        face = facelist[i - 1]
        top = top + " " + topstr
        topcenter = topcenter + " " + str(face[0])
        center = center + " " + str(face[1])
        bottomcenter = bottomcenter + " " + str(face[2])
        bottom = bottom + " " + btmstr
    print(f"{top}\n{topcenter}\n{center}\n{bottomcenter}\n{bottom}")
    return dicelist


def keep(keepl, items_to_add):
    for i in items_to_add:
        keepl.append(i)


def get_score(hand1, hand2, comp_or_prsn):
    hand_ranks = ["Five of a Kind", "Four of a Kind", "Full House", "Straight", "Three of a Kind", "Two Pair",
                  "One Pair", "Bust"]  # Added missing standard ranks

    def evaluate_hand(hand):
        if len(hand) != 5:
            return "Bust", (0, 0, 0, 0, 0)  # If hand is incomplete, treat as Bust with low tiebreakers

        sorted_hand = sorted(hand, reverse=True)  # Sort descending for tiebreakers
        counts = Counter(hand)
        count_values = sorted(counts.values(), reverse=True)
        unique_values = sorted(counts.keys(), reverse=True)

        # Check for Straight
        is_straight = (len(counts) == 5) and (sorted_hand[0] - sorted_hand[4] == 4)

        if count_values[0] == 5:
            rank = "Five of a Kind"
            tiebreak = (list(counts.keys())[0],)
        elif count_values[0] == 4:
            rank = "Four of a Kind"
            four_val = max(k for k, v in counts.items() if v == 4)
            single = next(k for k, v in counts.items() if v == 1)
            tiebreak = (four_val, single)
        elif count_values == [3, 2]:
            rank = "Full House"
            three_val = next(k for k, v in counts.items() if v == 3)
            pair_val = next(k for k, v in counts.items() if v == 2)
            tiebreak = (three_val, pair_val)
        elif is_straight:
            rank = "Straight"
            tiebreak = (sorted_hand[0],)  # High card
        elif count_values[0] == 3:
            rank = "Three of a Kind"
            three_val = next(k for k, v in counts.items() if v == 3)
            singles = sorted([k for k, v in counts.items() if v == 1], reverse=True)
            tiebreak = (three_val, singles[0], singles[1])
        elif count_values == [2, 2, 1]:
            rank = "Two Pair"
            pairs = sorted([k for k, v in counts.items() if v == 2], reverse=True)
            single = next(k for k, v in counts.items() if v == 1)
            tiebreak = (pairs[0], pairs[1], single)
        elif count_values[0] == 2:
            rank = "One Pair"
            pair_val = next(k for k, v in counts.items() if v == 2)
            singles = sorted([k for k, v in counts.items() if v == 1], reverse=True)
            tiebreak = (pair_val, singles[0], singles[1], singles[2])
        else:
            rank = "Bust"
            tiebreak = tuple(sorted_hand)

        return rank, tiebreak

    rank1, tie1 = evaluate_hand(hand1)
    rank2, tie2 = evaluate_hand(hand2)

    name = "Player 2" if comp_or_prsn == 1 else "Computer"

    print("FINAL HANDS:\n"
          f"Player 1: {hand1} ({rank1})\n"
          f"{name}: {hand2} ({rank2})\n")

    rank_idx1 = hand_ranks.index(rank1)
    rank_idx2 = hand_ranks.index(rank2)

    if rank_idx1 < rank_idx2:
        print("Player 1 wins!")
    elif rank_idx1 > rank_idx2:
        print(f"{name} wins!")
    else:
        # Compare tiebreakers
        if tie1 > tie2:
            print("Player 1 wins! (tiebreaker)")
        elif tie1 < tie2:
            print(f"{name} wins! (tiebreaker)")
        else:
            print("It's a tie!")


def player_turn(dice_rolls, keepl):
    dlist = show(keepl)
    dice_rolls = dice_rolls - 1
    play = [
        inquirer3.List("play", message="What would you like to do?", choices=["Keep Dice", "End Turn"])
    ]
    answer = inquirer3.prompt(play)

    if answer["play"] == "Keep Dice":
        newly_rolled_dice = dlist[len(keepl):]
        if newly_rolled_dice:
            keepquestion = [
                inquirer3.Checkbox("menu", message="Which dice would you like to keep?",
                                   choices=newly_rolled_dice)
            ]
            keepqa = inquirer3.prompt(keepquestion)
            print(f"Keeping {keepqa['menu']}")
            keep(keepl, keepqa["menu"])
        else:
            print("No unkept dice to keep!")

    return dice_rolls


def computer_turn(dice_rolls, keepl):
    show(keepl)

    return dice_rolls - 1


def player_vs_computer():
    p1keep = []
    ckeep = []
    p1dice_rolls = int(def_dice_rolls)
    cdice_rolls = int(def_dice_rolls)
    finished = False

    while not finished:
        if p1dice_rolls > 0:
            print(f"\n--- PLAYER 1 TURN ({p1dice_rolls} rolls left) ---")
        p1dice_rolls = player_turn(p1dice_rolls, p1keep)
        if cdice_rolls > 0:
            print(f"\n--- COMPUTER TURN ({cdice_rolls} rolls left) ---")
        cdice_rolls = computer_turn(cdice_rolls, ckeep)
        print("\n-------------------------")
        if p1dice_rolls == 0 and cdice_rolls == 0:
            finished = True
            print("Game Over!")
            get_score(p1keep, ckeep, 0)


def player_vs_player():
    p1keep = []
    p2keep = []
    p1dice_rolls = int(def_dice_rolls)
    p2dice_rolls = int(def_dice_rolls)
    finished = False

    while not finished:
        if p1dice_rolls > 0:
            print(f"\n--- PLAYER 1 TURN ({p1dice_rolls} rolls left) ---")
        p1dice_rolls = player_turn(p1dice_rolls, p1keep)
        if p2dice_rolls > 0:
            print(f"\n--- PLAYER 2 TURN ({p2dice_rolls} rolls left) ---")
        p2dice_rolls = player_turn(p2dice_rolls, p2keep)
        print("\n-------------------------")
        if p1dice_rolls == 0 and p2dice_rolls == 0:
            finished = True
            print("Game Over!")
            get_score(p1keep, p2keep, 1)


def main():
    menu = [
        inquirer3.List("menu", message="What mode would you like to play?", choices=["1 vs. Computer", "1 vs. 1"])
    ]
    menu_answers = inquirer3.prompt(menu)
    if menu_answers["menu"] == "1 vs. Computer":
        player_vs_computer()
    else:
        player_vs_player()


# test

while __name__ == '__main__':
    main()
