#! /usr/bin/python

## imports
import os, sys
from subprocess import Popen
from decimal import *

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
    j += """<div class="collumn">
    <div class="head"><span class="headline hl3">The Stock Report</span><p><span class="headline hl4">Polly Esther</span></p></div>
    <table style="width:100%">
  <tr>
    <th><b>Stock Symbol</th>
    <th>Company Name</th>
    <th>Price</b></th>
  </tr>
  <tr>
    <td>GE</td>
    <td>General Electric</td>
    <td>{GE}</td>
  </tr>
    <tr>
        <td>GM</td>
        <td>General Motors</td>
        <td>{GM}</td>
    </tr>
    <tr>
        <td>KO</td>
        <td>Coca-Cola</td>
        <td>{KO}</td>
    </tr>
    <tr>
        <td>IN</td>
        <td>Invincible Oil</td>
        <td>{IN}</td>
    </tr>
    <tr>
        <td>PT</td>
        <td>Pittsburgh Coal</td>
        <td>{PT}</td>
    </tr>
</table>
</p></div>\n""".format(**stockPrice)
    fmt_dict = {
        "title": "Nation Daily",
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

def updateStocks():
    global stockPrice
    with open('.days/%s' % date,'r') as k:
        dat = k.read().splitlines()
    stockPrice = {"GE" : dat[4],"GM" : dat[5],"KO" : dat[6],"IN" : dat[7],"PT" : dat[8]}

## init
with open('.resources/calendar', 'r') as f:
    cal = f.readlines()
run = True
money = 50000
date = 0
stockInv = {
    "GE" : 0,
    "GM" : 0,
    "KO" : 0,
    "IN" : 0,
    "PT" : 0,
}

stockPrice = {
    "GE" : 0,
    "GM" : 0,
    "KO" : 0,
    "IN" : 0,
    "PT" : 0,
}

nd = False

def play(sound):
    os.spawnlp(os.P_NOWAIT, 'afplay', 'afplay', '.resources/music/%s' % sound)

def clear():
    os.system('clear')

def save():
    open(".%s" % name, 'w').write("%s\n%s\n%s\n" % (money, date, stocks))

def quit():
    save()
    sys.exit("Goodbye!")

def report():
    print("")

def buy():
    global stocks
    print("Ask broker to buy what?")

def sell():
    global stocks
    print("Ask broker to sell what?")

def changeMoney(newVal, reason):
    global money
    if newVal > money:
        print("You got %s dollars from %s. Your new total is %s." % (float(newVal - money) / 100.0, reason, float(newVal)/100))
    else:
        print("You spent %s dollars on %s. Your new total is %s." % (float(money - newVal) / 100.0, reason, float(newVal)/100))
    money = newVal

def cPaper():
    play("operator.mp3")
    play("phone.aiff")
    print("What is your answer?")
    with open('.days/%s' % date,'r') as k:
        if raw_input().lower() == k.read().splitlines()[9]:
            print("You got it right! Your prize is 50 dollars!")
            changeMoney(money + 5000, "the newspaper")

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
    global money, date
    names = open('.resources/names', 'r').read().splitlines()
    print("Please enter your first name: ")
    user = raw_input().lower()
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
clear()
while run:
    play("alarm.mp3")
    updateStocks()
    print(writeNews())
    while not nd:
        options[menu()]()
    print("You call it a day and hit the hay.")
    nd = False
    date += 1
