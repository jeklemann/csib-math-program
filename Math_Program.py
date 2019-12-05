from tkinter import *
import random

easy_choices=["+","-"]
medium_choices=["+","-","*","/"]

def question(symbol):
    integer1 = random.randint(0, 10)
    integer2 = random.randint(0, 10)
    if symbol=="/":
        if integer2 == 0:
            integer2= random.randint(1, 10)
        print(integer1*integer2, symbol, integer2)
        answer=integer1
    else:
        print(integer1, symbol, integer2)
        answer=eval(str(integer1)+symbol+str(integer2))
    submited = input(" - ")
    if submited == str(answer):
        print("correct")

def easy():
    question(random.choice(easy_))
    
def medium():
    question(random.choice(medium_))
    
def hard():
    option1=random.choice(medium)
    option2=random.choice(medium)
    

