#! /usr/bin/python

## imports
import os, sys
from subprocess import Popen
from decimal import *

## file operations
def readPrice(url):
    return open('.prices/' + url, 'r').read().splitlines()
def writeReport():
    with open('.report/index.html','w') as f:
        f.write("""
        <html>
        <link rel="stylesheet" href="css/style.css">
        <head><title>Report</title>Stock Report for %s<p></head>
        <body>Inventory:
          <ul style="list-style-type:none">
          <li>GE: %s = %s</li>
          <li>GM: %s = %s</li>
          <li>KO: %s = %s</li>
          <li>IN: %s = %s</li>
          <li>PT: %s = %s</li>
        </ul>
        Money: %s<p>
        Assets: %s<p>
        <div class="imageContainer">Total: %s</div>
        </body>
        </html>""" % (cal[date],stockInv["GE"],stockInv["GE"]*stockPrice["GE"],stockInv["GM"],stockInv["GM"]*stockPrice["GM"],stockInv["KO"],stockInv["KO"]*stockPrice["KO"],stockInv["IN"],stockInv["IN"]*stockPrice["IN"],stockInv["PT"],stockInv["PT"]*stockPrice["PT"],money,stockInv["GE"]*stockPrice["GE"]+stockInv["GM"]*stockPrice["GM"]+stockInv["KO"]*stockPrice["KO"]+stockInv["IN"]*stockPrice["IN"]+stockInv["PT"]*stockPrice["PT"],money+stockInv["GE"]*stockPrice["GE"]+stockInv["GM"]*stockPrice["GM"]+stockInv["KO"]*stockPrice["KO"]+stockInv["IN"]*stockPrice["IN"]+stockInv["PT"]*stockPrice["PT"]))
def writeNews():
    global money
    with open('.days/%s' % date,'r') as k:
        data = k.read().splitlines()
    loc = data[1]
    dat = cal[date]
    ln = data[2]
    price = data[3]
    money -= int(filter(str.isdigit, price)) / 100
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
        &ensp;{text}</p></div>\n""".format(**indv)
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
    stockPrice = {"GE" : int(dat[4]),"GM" : int(dat[5]),"KO" : int(dat[6]),"IN" : int(dat[7]),"PT" : int(dat[8])}

## init
with open('.resources/calendar', 'r') as f:
    cal = f.readlines()
q = False
run = True
money = Decimal(500.00)
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

##def save():
##    open(".%s" % name, 'w').write("%s\n%s\n%s\n" % (money, date, stocks))

def quit():
##    save()
    sys.exit("Goodbye!")

def report():
    writeReport()
    display('.report/index.html')

def buy():
    global stockInv
    print("Ask broker to buy what?")
    sel = raw_input()
    if sel in stockInv:
        print("How many shares? (Max %s)" % (int(money / stockPrice[sel])))
        num = raw_input()
        try:
            if int(num) < 0:
                print("You can't buy negative shares!")
                return
            if stockPrice[sel] * int(num) <= money:
                stockInv[sel] += int(num)
                changeMoney((money - stockPrice[sel] * int(num)), "%s shares of %s, giving you a total of %s shares" % (num, sel, stockInv[sel]))
            else:
                print("You don't have enough money!")
        except ValueError:
            print("I don't understand what you mean. Please use positive integers.")
    else:
        print("I'm sorry, I don't know what you mean. Please use the stock symbols found in the newspaper.")

def sell():
    global stockInv
    print(stockPrice)
    print(money)
    print("Ask broker to sell what?")
    sel = raw_input()
    if sel in stockInv:
        print("How many shares? (Max %s)" % (stockInv[sel]))
        num = raw_input()
        try:
            if int(num) < 0:
                print("You can't sell negative shares!")
                return
            if int(num) >= stockInv[sel]:
                stockInv[sel] -= int(num)
                changeMoney((money + stockPrice[sel] * int(num)), "%s shares of %s, giving you a total of %s shares" % (num, sel, stockInv[sel]))
            else:
                print("You don't have enough money!")
        except ValueError:
            print("I don't understand what you mean. Please use positive integers.")
    else:
        print("I'm sorry, I don't know what you mean. Please use the stock symbols found in the newspaper.")


def changeMoney(newVal, reason):
    global money
    if newVal > money:
        print("You got %s dollars from %s. Your new balance is %s." % (newVal - money, reason, newVal))
    else:
        print("You spent %s dollars on %s. Your new balance is %s." % (money - newVal, reason, newVal))
    money = Decimal(newVal.quantize(Decimal('.01'), rounding=ROUND_DOWN))

def cPaper():
    global q
    play("operator.mp3")
    play("phone.aiff")
    if not q:
        q = True
        print("What is your answer?")
        with open('.days/%s' % date,'r') as k:
            if raw_input().lower() == k.read().splitlines()[9]:
                print("You got it right! Your prize is 50 dollars!")
                changeMoney(money + 50, "the newspaper")
            else:
                print("I'm sorry, the correct answer was %s. Better luck next time!" % k.read().splitlines()[9])
    else:
        print("You've already called us today! Only one attempt allowed per day.")

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
