from tkinter import *
import tkinter
import random

window = Tk()
window.title("Math Tutor")

Title = Label(window, text="Math Tutor")
Title.grid(column=1,row=0)

question_text = StringVar("")
question = Label(window, textvariable=question_text)
question.grid(column=1,row=2)

answer_submitted = Entry(window, width=5)
answer_submitted.grid(column=1,row=3)

result = Label(window, text="")
result.grid(column=2,row=3)

easy_choices=["+","-"]
medium_choices=["+","-","*","/"]
answer=None
question_asked=None

def check(null_arg):
    global answer
    global question_asked
    if answer!=None:
        if str(answer)==answer_submitted.get():
            result = Label(window, text="✓")
            result.grid(column=2,row=3)
        else:
            result = Label(window, text="X")
            result.grid(column=2,row=3)
    if question_asked!=None:
        exec(question_asked)
    answer_submitted.delete(0,END)
    
def question(symbol):
    global answer
    integer1 = random.randint(0, 10)
    integer2 = random.randint(0, 10)
    if symbol=="/":
        if integer2 == 0:
            integer2 = random.randint(1, 10)
        question_text.set((integer1*integer2, symbol, integer2))
        answer=integer1
    else:
        question_text.set((integer1, symbol, integer2))
        answer=eval(str(integer1)+symbol+str(integer2))

def question_hard(symbol1,symbol2):
    global answer
    integer1 = random.randint(0, 10)
    integer2 = random.randint(0, 10)
    integer3 = random.randint(0, 10)
    if symbol1=="/":
        if symbol2=="/":
            if integer2 == 0:
                integer2 = random.randint(1, 10)
            if integer3 == 0:
                integer3 = random.randint(1, 10)
            question_text.set(("(",integer1*integer2*integer3, symbol1, integer2,")", symbol2, integer3))
            answer=integer1
        else:
            if integer2 == 0:
                integer2 = random.randint(1, 10)
            question_text.set(("(",integer1*integer2, symbol1, integer2,")", symbol2, integer3))
            answer=eval("("+str(integer1*integer2)+symbol1+str(integer2)+")"+symbol2+str(integer3))
    else:
        if symbol2=="/":
            if integer3 == 0:
                integer3 = random.randint(1, 10)
            question_text.set(("(",integer1*integer3, symbol1, integer2*integer3,")", symbol2, integer3))
            answer=eval("("+str(integer1*integer3)+symbol1+str(integer2*integer3)+")"+symbol2+str(integer3))
        else:
            question_text.set(("(",integer1, symbol1, integer2,")", symbol2, integer3))
            answer=eval("("+str(integer1)+symbol1+str(integer2)+")"+symbol2+str(integer3))

def easy_question():
    global question_asked
    question_asked="easy_question()"
    question(random.choice(easy_choices))
    
def medium_question():
    global question_asked
    question_asked="medium_question()"
    question(random.choice(medium_choices))
    
def hard_question():
    global question_asked
    question_asked="hard_question()"
    question_hard(random.choice(medium_choices),random.choice(medium_choices))

easy = Button(window, text="Easy", command=easy_question)
medium = Button(window, text="Medium", command=medium_question)
hard = Button(window, text="Hard", command=hard_question)
easy.grid(column=0,row=1)
medium.grid(column=1,row=1)
hard.grid(column=2,row=1)

window.bind('<Return>', check)
