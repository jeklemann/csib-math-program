from tkinter import *
import tkinter
import random
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
            score+=risk
        else:
            result = Label(window, text="X")
            result.grid(column=2,row=3)
            score-=risk
    if question_asked!=None:
        exec(question_asked)
    answer_submitted.delete(0,END)
    update_entry(conn, score)
    
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
