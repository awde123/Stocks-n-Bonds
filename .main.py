#! /usr/bin/python

## imports
import os, sys
from subprocess import Popen

## file operations
def readPrice(url):
    return open('.prices/' + url, 'r').read().splitlines()
def writeNews():
    with open('.days/%s' % date,'r') as k:
        data = k.read().splitlines()
    loc = data[1]
    dat = cal[date]
    ln = data[2]
    price = data[3]
    with open('.days/%s.ar' % date, 'r') as w:
        art = w.read().splitlines()
    j = ""
    for i in art:
        indv = {
        "title" : i.split("#")[0],
        "author" : "By " + i.split("#")[1],
        "text": i.split("#")[2],
        }
        j += """<div class="collumn">
        <div class="head"><span class="headline hl3">{title}</span><p><span class="headline hl4">{author}</span></p></div>
        {text}</p></div>\n""".format(**indv)
    fmt_dict = {
        "title": "Today's Paper",
        "square": "The best news ever",
        "loc" : loc,
        "date" : dat,
        "length" : ln,
        "art": j,
        "price": price,
    }
    text = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
    <html>
    <head>
    <title>{title}</title>
    <meta name="viewport" content="width=device-width">
    </head>
    <body>
    <div class="head">
        <div class="headerobjectswrapper">
            <header>{title}</header>
        </div>
        <div class="subhead">{loc} - {date} - {length}<span class="price">{price}</div><div style="clear: both;"></div>
    </div>
    <div class="content">
        <div class="collumns">
            {art}
        </div>
    </div>
    </body>
    </html>
    """.format(**fmt_dict)
    with open('.news/index.html', 'w') as f:
        f.write(text)
    return data[0]


def display(url):
    os.system("open " + url)

def dispnews():
    display('.news/index.html')

## init
with open('.resources/calendar', 'r') as f:
    cal = f.readlines()
run = True
money = 0
date = 0
score = 0
stocks = {}
nd = False

def play(sound):
    os.spawnlp(os.P_NOWAIT, 'afplay', 'afplay', '.resources/music/%s' % sound)

def clear():
    os.system('clear')

def save():
    open(".%s" % name, 'w').write("%s\n%s\n%s\n%s\n" % (money, date, score, stocks))

def quit():
    save()
    sys.exit("Goodbye!")

def report():
    print("WIP")

def buy():
    print("WIP")

def sell():
    print("WIP")

def short():
    print("WIP")

def cPaper():
    play("operator.mp3")
    play("phone.aiff")

def endDay():
    global nd
    nd = True

options = {
    0 : quit,
    1 : report,
    2 : buy,
    3 : sell,
    4 : dispnews,
    5 : cPaper,
    6 : endDay,
}

## user interface
def name():
    global money, date, score
    names = open('.resources/names', 'r').read().splitlines()
    print("Please enter your first name: ")
    user = raw_input()
    if not user in names:
        print("I don't see you on my list")
        return name()
    return user

def menu():
    print("#############")
    print("Report      1")
    print("Buy         2")
    print("Sell        3")
    print("Read paper  4")
    print("Call paper  5")
    print("Go to sleep 6")
    print("Quit        0")
    sel = raw_input()
    if sel.isdigit():
        if (int(sel) < 7) and (int(sel) > -1):
            clear()
            return int(sel)
    clear()
    print("Please enter a valid selection...")
    return menu()

## execution
clear()
name = name()
while run:
    play("alarm.mp3")
    print(writeNews())
    while not nd:
        options[menu()]()
    print("You call it a day and hit the hay.")
    nd = False
    date += 1
