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


def keep(keepl, keeplist, dicelist):
    for i in keeplist:
        keepl.append(i)


def player_turn(dice_rolls, keepl):
    dlist = show(keepl)
    dice_rolls = dice_rolls - 1
    play = [
        inquirer3.List("play", message="What would you like to do?", choices=["Keep Dice", "End Turn"])
    ]
    answer = inquirer3.prompt(play)

    if answer["play"] == "Keep Dice":
        keeplist = []
        keepcl = []

        for i in dlist:
            if dlist.index(i) > (len(keeplist) - 1):
                keepcl.append(i)

        keepquestion = [
            inquirer3.Checkbox("menu", message="Which dice would you like to keep?",
                               choices=keepcl)
        ]
        keepqa = inquirer3.prompt(keepquestion)
        print(keepqa["menu"])
        keep(keepl, keeplist, dlist)


def computer_turn(dice_rolls, keepl):
    show(keepl)


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
        print("PLAYER 1 TURN")
        player_turn(p1dice_rolls, p1keep)
        print(p1keep)
        print("PLAYER 2 TURN")
        player_turn(p2dice_rolls, p2keep)
        print(p2keep)
        if p1dice_rolls & p2dice_rolls == 0:
            finished = True


def main():
    menu = [
        inquirer3.List("menu", message="What mode would you like to play?", choices=["1 vs. Computer", "1 vs. 1"])
    ]
    menu_answers = inquirer3.prompt(menu)
    if menu_answers["menu"] == "1 vs. Computer":
        player_vs_computer()
    else:
        player_vs_player()


if __name__ == '__main__':
    main()
