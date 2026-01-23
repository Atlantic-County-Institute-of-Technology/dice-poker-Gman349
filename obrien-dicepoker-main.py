# imports
import inquirer3
from dice import *

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

    hand_ranks = ["Five of Kind", "Four of Kind", "Full House", "Two Pair", "One Pair", "Bust"]

    name = ""
    if comp_or_prsn == 1:
        name = 'Player 2:'
    else:
        name = 'Computer'
    print("FINAL HANDS:\n"
          f"Player 1:{hand1}\n"
          f"{name}{hand2}\n")


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
    dice_rolls = int(def_dice_rolls)
    cdice_rolls = int(def_dice_rolls)
    finished = False
    while not finished:
        player_turn(dice_rolls, p1keep)
        computer_turn(cdice_rolls, ckeep)
        if dice_rolls & cdice_rolls == 0:
            finished = True


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
#test

while __name__ == '__main__':
    main()
