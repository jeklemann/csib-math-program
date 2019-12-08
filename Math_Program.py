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

def question_hard(symbol1,symbol2):
    integer1 = random.randint(0, 10)
    integer2 = random.randint(0, 10)
    integer3 = random.randint(0, 10)
    if symbol1=="/":
        if symbol2=="/":
            print("(",integer1*integer2*integer3, symbol1, integer2,")", symbol2, integer3)
            answer=integer1
        else:
            print("(",integer1*integer2, symbol1, integer2,")", symbol2, integer3)
            answer=eval("("+str(integer1*integer2)+symbol1+str(integer2)+")"+symbol2+str(integer3))
    else:
        if symbol2=="/":
            print("(",integer1*integer3, symbol1, integer2*integer3,")", symbol2, integer3)
            answer=eval("("+str(integer1*integer3)+symbol1+str(integer2*integer3)+")"+symbol2+str(integer3))
        else:
            print("(",integer1, symbol1, integer2,")", symbol2, integer3)
            answer=eval("("+str(integer1)+symbol1+str(integer2)+")"+symbol2+str(integer3))
    submited = input(" - ")
    if submited == str(answer):
        print("correct")
def easy():
    question(random.choice(easy_choices))
    
def medium():
    question(random.choice(medium_choices))
    
def hard():
    question_hard(random.choice(medium_choices),random.choice(medium_choices))

    

