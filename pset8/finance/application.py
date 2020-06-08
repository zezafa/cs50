import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

"""
# TODO
 - streamline all names in database fx userId, persId etc.
 - improve redundacy (way to many request.form calls)
"""

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rowsC = db.execute("SELECT * FROM current WHERE userId = :id", id = session["user_id"])
    rowsU = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])

    # Append values in dictionaries to a new index list
    index = []
    # counter (TODO do it with enumrate func)
    i = 0

    for row in rowsC:
        # a "bit" ugly (#todo)
        # declare a new dic
        index.append({})
        symbol = row["stock"]

        amount = row["shares"]

        # look up func
        query = lookup(row["stock"])

        name = query["name"]

        unitPrice = query["price"]

        totalPrice = float(amount) * float(unitPrice)

        index[i]["symbol"] = symbol
        index[i]["name"] = name
        index[i]["amount"] = amount
        index[i]["unitPrice"] = unitPrice
        index[i]["totalPrice"] = totalPrice

        # increase counter
        i = i + 1

    cash = rowsU[0]["cash"]

    sumTotal = 0
    for i in index:
        sumTotal = sumTotal + i["totalPrice"]

    totalAssets = cash + sumTotal

    return render_template("index.html", index = index, cash = cash, totalAssets = totalAssets)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("please enter the stock symbol")

        # Check if share amount is an int
        if not request.form.get("shares").isdigit():
            return apology("please enter an amount")

        # Check if share amount is positive
        if int(request.form.get("shares")) <= 0:
            return apology("please enter a positive and non-zero share amount")

        if lookup(request.form.get("symbol")) is not None:
            # Find stock
            stock = lookup(request.form.get("symbol"))
            # Calculate total price for transaction
            price = float(stock["price"]) * float(request.form.get("shares"))
            # Find the amount of cash Wowned by person
            pers = db.execute("SELECT * FROM users WHERE id = :id",
                                id = session["user_id"])[0]
            cash = float(pers["cash"])
            cash = cash - price
            # See if user can afford transaction and update database
            if cash >= 0:
                db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                            cash = cash,
                            id = session["user_id"])

                # Update history database
                db.execute("INSERT INTO history (persId, stock, amount, price) VALUES (?, ?, ?, ?)",
                            session["user_id"],
                            request.form.get("symbol"),
                            request.form.get("shares"),
                            stock["price"])

                # Update current database (bug: amount = shares #todo)
                # TODO a bug: if there are more shares with same name, they will be updated
                #             better design would be: SQL sort by name, take the first field and update it
                rows = db.execute("SELECT stock FROM current WHERE userId = :id", id = session["user_id"])
                boo = 0
                for field in rows:
                    print("we are in buy")
                    if (request.form.get("symbol").upper() in field["stock"] and boo == 0) :
                        db.execute("UPDATE current SET shares = shares + :amount WHERE stock = :stock AND userId = :id",
                                    amount = request.form.get("shares"),
                                    stock = request.form.get("symbol"),
                                    id = session["user_id"])
                        boo = 1
                if boo == 0:
                    db.execute("INSERT INTO current (userId, stock, shares) VALUES (?, ?, ?)",
                                session["user_id"],
                                request.form.get("symbol"),
                                request.form.get("shares"))

                # Redirect user to home page
                return redirect("/")
            else:
                return apology("insufficient funds")
        else:
            return apology("stock not found")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM history WHERE persId = :id", id = session["user_id"])
    return render_template("history.html", rows = rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("please enter the stock symbol")

        if lookup(request.form.get("symbol")) is not None:
            stock = lookup(request.form.get("symbol"))
            return render_template("quoted.html", stock=stock["name"], symbol=stock["symbol"], price=stock["price"])
        else:
            return apology("stock not found")
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if session.get("user_id") is not None:
        return apology("log off to create new user.")

    #Forget any user_id just to be sure
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Query database for username and check if it is already used
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                            username = request.form.get("username"))
        if len(rows) != 0:
            return apology("username already exists")

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")

        # Ensure that passwords do match
        if (request.form.get("password") != request.form.get("confirmation")):
            return apology("passwords must match")

        # Ensure that password are at least 8 letters
        if (len(request.form.get("password")) < 8):
            return apology("password must be at least 8 letters")

        # Ensure that password includes at least two symbols and no white spaces
        if len([x for x in request.form.get("password") if x.isdigit()]) < 2:
            return apology("password must contain at least 2 digits")

        # Ensure that password has no whitespaces
        if " " in request.form.get("password"):
            return apology("password must not contain whitespaces")

        # Insert username and psw hash into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                    request.form.get("username"),
                    generate_password_hash(request.form.get("password")))

        # Redirecrt user to login page
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("please enter the stock symbol")

        # Check if share amount is an int
        if not request.form.get("shares").isdigit():
            return apology("please enter an amount")

        # Check if share amount is positive
        if int(request.form.get("shares")) <= 0:
            return apology("please enter a positive and non-zero share amount")

        rows = db.execute("SELECT stock FROM current WHERE userId = :id", id = session["user_id"])
        boo = 0
        for field in rows:
            if (request.form.get("symbol").upper() in field["stock"] and boo == 0):
                boo = 1

        if boo == 0:
            return apology("you do not own the stock")

        if lookup(request.form.get("symbol")) is not None:
            # Find stock user
            stock = lookup(request.form.get("symbol"))
            # Calculate total price for transaction
            price = float(stock["price"]) * float(request.form.get("shares"))
            # Find the amount of cash owned by person
            pers = db.execute("SELECT * FROM users WHERE id = :id",
                                id = session["user_id"])[0]
            cash = float(pers["cash"])
            cash = cash + price

            # Update current database
            row = db.execute("SELECT * FROM current WHERE userId = :id AND stock = :symbol",
                            id = session["user_id"],
                            symbol = request.form.get("symbol").upper())
            if row[0]["shares"] == int(request.form.get("shares")):
                db.execute("DELETE FROM current WHERE userId = :id AND stock = :symbol",
                            id = session["user_id"],
                            symbol = request.form.get("symbol").upper())
            elif row[0]["shares"] < int(request.form.get("shares")):
                return apology("you do not own enough shares")
            else:
                # to do
                print(request.form.get("shares"))
                print("we are in sell")
                temp = row[0]["shares"] - int(request.form.get("shares"))
                db.execute("UPDATE current SET shares = :amount WHERE stock = :stock AND userId = :id",
                            amount = temp,
                            stock = request.form.get("symbol"),
                            id = session["user_id"])

            # Update current cash
            db.execute("UPDATE users SET cash = :cash WHERE id = :id",
                        cash = cash,
                        id = session["user_id"])

            temp = int(request.form.get("shares")) * -1

            # Update history database
            db.execute("INSERT INTO history (persId, stock, amount, price) VALUES(?, ?, ?, ?)",
                        session["user_id"],
                        request.form.get("symbol"),
                        temp,
                        stock["price"])

            return redirect("/")
        else:
            return apology("stock not found by lookup")
        # TODO get method


    return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
