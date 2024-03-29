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
Title.grid(column=2,row=0)

question_text = StringVar("")
question = Label(window, textvariable=question_text)
question.grid(column=2,row=2)

answer_submitted = Entry(window, width=5)
answer_submitted.grid(column=2,row=3)

time_taken = StringVar("")
time_measure = Label(window, textvariable=time_taken)
time_measure.grid(column=1,row=3)

correct = StringVar("")
result = Label(window, textvariable=correct)
result.grid(column=3,row=3)

progress_bar = Progressbar(window, length=200)
progress_bar.grid(column=2,row=4)

scoreval = IntVar()
scoreval.set(score)
scorelabel = Label(window, textvariable=scoreval)
scorelabel.grid(column=2, row=5)

easy_choices=["+","-"]
medium_choices=["+","-","*","/","|"]
hard_choices=["+","-","*","/"]
estimation_choices=["√","/"]
other_choices=["!","median","mean","mode"]
answer=None
question_asked=None
time_start=None
question_weights={"easy_question()":"1","medium_question()":"3","hard_question()":"20","estimation_question()":"10","other_question()":"15"}

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
    elif symbol=="|":
        abs_integer = random.randint(-30, 30)
        question_text.set((symbol, abs_integer, symbol))
        answer=abs(abs_integer)
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

def question_estimation(symbol):
    global answer
    global time_start
    time_start=time.time()
    if symbol == "√":
        integer = random.randint(1,10)
        question_text.set(("√",integer))
        answer=int(math.sqrt(integer))
    if symbol == "/":
        integer1 = random.randint(0,100)
        integer2 = random.randint(1,10)
        question_text.set((integer1,"/",integer2))
        answer=round(integer1/integer2)

def question_other(symbol):
    global answer
    global time_start
    time_start=time.time()
    if symbol=="!":
        integer=random.randint(1,5)
        question_text.set((integer,"!"))
        answer=math.factorial(int(integer))
    if symbol=="median":
        interger1=random.randint(1,100)
        interger2=random.randint(1,100)
        interger3=random.randint(1,100)
        interger4=random.randint(1,100)
        interger5=random.randint(1,100)
        median_list=[interger1,interger2,interger3,interger4,interger5]
        median_list.sort()
        answer=median_list[2]
        question_text.set(("median : "+str(median_list)[1:-1]))
    if symbol=="mean":
        integer1=random.randint(1,100)
        integer2=random.randint(1,100)
        integer3=random.randint(1,100)
        mean_list=[integer1,integer2,integer3]
        mean_list.sort()
        answer=int(integer1+integer2+integer3/3)
        question_text.set(("mean : "+str(mean_list)[1:-1]))
    if symbol=="mode":
        integer1=random.randint(51,100)
        integer2=random.randint(1,50)
        integer3=random.randint(1,100)
        mode_list=[integer1,integer2,integer3,integer3]
        mode_list.sort()
        answer=integer3
        question_text.set(("mode : "+str(mode_list)[1:-1]))

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
    question_hard(random.choice(hard_choices),random.choice(hard_choices))
def estimation_question():
    global question_asked
    global risk
    risk = 5
    question_asked="estimation_question()"
    question_estimation(random.choice(estimation_choices))
def other_question():
    global question_asked
    global risk
    risk = 5
    question_asked="other_question()"
    question_other(random.choice(other_choices))

easy = Button(window, text="Easy", command=easy_question)
medium = Button(window, text="Medium", command=medium_question)
hard = Button(window, text="Hard", command=hard_question)
estimation = Button(window, text="Estimations", command=estimation_question)
other = Button(window, text="Other", command=other_question)
estimation.grid(column=0,row=1)
easy.grid(column=1,row=1)
medium.grid(column=2,row=1)
hard.grid(column=3,row=1)
other.grid(column=4, row=1)

window.bind('<Return>', check)
