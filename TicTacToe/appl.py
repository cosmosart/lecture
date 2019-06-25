from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

"""
First Flask App
"""


app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def wCheck(aList):
    if aList[0] != None and aList[0] == aList[1] == aList[2]:
        return True

@app.route("/")
def index():
    if "board" not in session:
        session["board"] = [[None, None, None],[None, None, None],[None, None, None]]
        session["turn"] = "X"
        session["message"] = 0
    return render_template("game.html", game=session['board'], turn = session['turn'], gamemessage = session["message"])
@app.route("/resetgame")
def resetgame():
    del session["board"]
    return redirect(url_for("index"))
@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    if session["message"] >= 9:
        return redirect(url_for("index"))
    session["board"][row][col] = session["turn"]
    for i in range(3):
        a = session['board'][i]
        b = [a[i] for a in session['board']]
        if wCheck(a) or wCheck(b):
                session["message"] = 10
    c = [session['board'][i][i] for i in range(3)]
    d = [session['board'][0][2],session['board'][1][1],session['board'][2][0]]
    if wCheck(c) or wCheck(d):
        session["message"] = 10
    if session["message"] == 10:
        return redirect(url_for("index"))                   
    if session["turn"] == "X": session["turn"] = "O"
    else: session["turn"] = "X"
    session["message"] += 1
    return redirect(url_for("index"))