from tkinter import *
import tkinter
from tkinter.ttk import Progressbar
import random
import time
import math
import sqlite3
from sqlite3 import Error

store_filename = r"scores.db"

username = open("username.txt").readline()
print(username)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

def create_table(conn, cmd):
    try:
        c = conn.cursor()
        c.execute(cmd)
    except Error as e:
        print(e)

def update_entry(conn, score):
    cmd = """REPLACE INTO scores
    (name, score)
VALUES
    (?, ?);"""
    curs = conn.cursor()
    curs.execute(cmd, (username, score))
    conn.commit()

def get_score(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM scores")
 
    row = cur.fetchone()
 
    if row == None:
        update_entry(conn, 0)
        return 0
    return row[1]
 
conn = create_connection(store_filename)

sql_create_table_cmd = """CREATE TABLE IF NOT EXISTS scores (
                                    name text NOT NULL PRIMARY KEY,
                                    score integer
                                );"""

if conn is not None:
    create_table(conn, sql_create_table_cmd)
else:
    print("Database could not accessed. Exiting")
    exit()

score = get_score(conn)
risk = 1

window = Tk()
window.title("Math Tutor")

Title = Label(window, text="Math Tutor")
Title.grid(column=1,row=0)

question_text = StringVar("")
question = Label(window, textvariable=question_text)
question.grid(column=1,row=2)

answer_submitted = Entry(window, width=5)
answer_submitted.grid(column=1,row=3)

time_taken = StringVar("")
time_measure = Label(window, textvariable=time_taken)
time_measure.grid(column=0,row=3)

correct = StringVar("")
result = Label(window, textvariable=correct)
result.grid(column=2,row=3)

progress_bar = Progressbar(window, length=200)
progress_bar.grid(column=1,row=4)

scoreval = IntVar()
scoreval.set(score)
scorelabel = Label(window, textvariable=scoreval)
scorelabel.grid(column=1, row=5)

easy_choices=["+","-"]
medium_choices=["+","-","*","/"]
answer=None
question_asked=None
time_start=None
question_weights={"easy_question()":"1","medium_question()":"3","hard_question()":"20"}

def check(null_arg):
    global answer
    global scoreval
    global score
    global question_asked
    global time_start
    global risk
    if time_start!=None:
        time_taken.set((str(int(time.time()-time_start)),"s"))
    if answer!=None:
        if str(answer)==answer_submitted.get():
            correct.set("✓")
            if question_asked!=None:
                progress_bar["value"]+=math.ceil(int(question_weights[question_asked])/int(eval(time_taken.get())[0]))
            score+=risk
        else:
            correct.set("X")
            score-=risk
    answer_submitted.delete(0,END)
    if question_asked!=None:
        exec(question_asked)
    scoreval.set(score)
    update_entry(conn, score)

def question(symbol):
    global answer
    global time_start
    time_start=time.time()
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
    global time_start
    integer1 = random.randint(0, 10)
    integer2 = random.randint(0, 10)
    integer3 = random.randint(0, 10)
    time_start=time.time()
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
            answer=eval(str(integer1)+symbol2+str(integer3))
    else:
        if symbol2=="/":
            if integer3 == 0:
                integer3 = random.randint(1, 10)
            question_text.set(("(",integer1*integer3, symbol1, integer2*integer3,")", symbol2, integer3))
            answer=int(eval("("+str(integer1*integer3)+symbol1+str(integer2*integer3)+")"+symbol2+str(integer3)))
        else:
            question_text.set(("(",integer1, symbol1, integer2,")", symbol2, integer3))
            answer=int(eval("("+str(integer1)+symbol1+str(integer2)+")"+symbol2+str(integer3)))

def easy_question():
    global question_asked
    global risk
    risk = 1
    question_asked="easy_question()"
    question(random.choice(easy_choices))
    
def medium_question():
    global question_asked
    global risk
    risk = 3
    question_asked="medium_question()"
    question(random.choice(medium_choices))
    
def hard_question():
    global question_asked
    global risk
    risk = 5
    question_asked="hard_question()"
    question_hard(random.choice(medium_choices),random.choice(medium_choices))

easy = Button(window, text="Easy", command=easy_question)
medium = Button(window, text="Medium", command=medium_question)
hard = Button(window, text="Hard", command=hard_question)
easy.grid(column=0,row=1)
medium.grid(column=1,row=1)
hard.grid(column=2,row=1)

window.bind('<Return>', check)
