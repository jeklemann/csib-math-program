from tkinter import *
import random

easy=["Addition","Subtraction"]
medium=["Addition","Subtraction","Multiplication","Divison"]

def addition():
    integer1 = random.randint(0, 10)
    integer2 = random.randint(0, 10)
    print(integer1, "+", integer2)
    answer = input(" - ")
    if answer == integer1 + integer2:
        print("correct")

def subtraction():
    integer1 = random.randint(0, 10)
    integer2 = random.randint(0, 10)
    print(integer1, "-", integer2)
    answer = input(" - ")
    if answer == integer1 - integer2:
        print("correct")


def multiplication():
    integer1 = random.randint(0, 10)
    integer2 = random.randint(0, 10)
    print(integer1, "*", integer2)
    answer = input(" - ")
    if answer == integer1 * integer2:
        print("correct")

def division():
    return
#easy
option=random.choice(easy)
if option="Addition":
    addition()

