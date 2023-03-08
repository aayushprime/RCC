import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get all users stock holdings
    rows = db.execute(
        "SELECT * FROM portfolio WHERE userid = :id", id=session["user_id"]
    )
    # get users account balance
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

    # get cash value float
    cash = cash[0]["cash"]
    # this will be total value of all stock holdings and cash
    sum = cash

    # add stock name, add current lookup value, add total value
    for row in rows:
        look = lookup(row["symbol"])
        row["name"] = look["name"]
        row["price"] = look["price"]
        row["total"] = row["price"] * row["shares"]

        # increment sum
        sum += row["total"]

        # convert price and total to usd format
        row["price"] = usd(row["price"])
        row["total"] = usd(row["total"])

    return render_template("index.html", rows=rows, cash=usd(cash), sum=usd(sum))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        elif not request.form.get("shares"):
            return apology("must provide shares", 403)

        symbol = request.form.get("symbol").upper()

        if request.form.get("shares").isdigit() == False:
            return apology("must provide valid number of shares", 400)

        shares_as_int = int(request.form.get("shares"))
        if shares_as_int < 1 or shares_as_int != float(request.form.get("shares")):
            return apology("must provide valid number of shares", 400)

        shares = int(request.form.get("shares"))
        unit_price = lookup(symbol)

        if unit_price == None:
            return apology("invalid stock symbol", 400)

        total = unit_price["price"] * shares

        # get the users account balance
        account_balance = db.execute(
            "SELECT cash FROM users WHERE id = :id", id=session["user_id"]
        )
        account_balance = account_balance[0]["cash"]

        if total > account_balance:
            return apology("insufficient funds", 403)

        # check if the user already has shares of the stock
        # query portfolio table for row with this userid and stock symbol:
        row = db.execute(
            "SELECT * FROM portfolio WHERE userid = :id AND symbol = :symbol",
            id=session["user_id"],
            symbol=symbol,
        )

        # if row doesn't exist yet, create it but don't update shares
        if len(row) != 1:
            db.execute(
                "INSERT INTO portfolio (userid, symbol) VALUES (:id, :symbol)",
                id=session["user_id"],
                symbol=symbol,
            )

        # get previous number of shares owned
        oldshares = db.execute(
            "SELECT shares FROM portfolio WHERE userid = :id AND symbol = :symbol",
            id=session["user_id"],
            symbol=symbol,
        )
        oldshares = oldshares[0]["shares"]

        # add purchased shares to previous share number
        newshares = oldshares + shares

        # update shares in portfolio table
        db.execute(
            "UPDATE portfolio SET shares = :newshares WHERE userid = :id AND symbol = :symbol",
            newshares=newshares,
            id=session["user_id"],
            symbol=symbol,
        )

        # update cash balance in users table
        db.execute(
            "UPDATE users SET cash = :remainder WHERE id = :id",
            remainder=account_balance - total,
            id=session["user_id"],
        )

        # update history table
        db.execute(
            "INSERT INTO history (userid, symbol, shares, method, price) VALUES (:userid, :symbol, :shares, 'Buy', :price)",
            userid=session["user_id"],
            symbol=symbol,
            shares=shares,
            price=unit_price["price"],
        )

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute(
        "SELECT * FROM history WHERE userid = :userid", userid=session["user_id"]
    )

    # return history template
    return render_template("history.html", rows=rows)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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

    if request.method == "POST":
        # try to get the symbol from the IEX API
        symbol = lookup(request.form.get("symbol"))

        # if symbol is None, return apology
        if symbol == None:
            return apology("invalid stock symbol", 400)

        if symbol == "":
            return apology("must provide symbol", 400)

        # Return the template quote
        return render_template("quoted.html", symbol=symbol)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        print(
            "POST",
            "$" + request.form.get("username") + "$",
            type(request.form.get("username")),
        )
        if request.form.get("username") == "":
            return apology("must provide username", 400)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # check if the password fields have the same password
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology(
                "confirm password field must have the same password as the password field",
                400,
            )

        user = request.form.get("username")
        password = request.form.get("password")

        # require users to have at least one number in their password
        if not any(char.isdigit() for char in password):
            return apology("password must contain at least one number", 400)
        # require users to have at least one symbol in their password
        if not any(not char.isalnum() for char in password):
            return apology("password must contain at least one symbol", 400)

        hash = generate_password_hash(password)

        # Query database for username to see if it is already taken
        rows = db.execute(
            "SELECT * FROM users WHERE username = :username", username=user
        )

        # if username is not taken, insert the new user into the database
        if len(rows):
            return apology("username already taken", 400)

        db.execute(
            "INSERT INTO users (username, hash) VALUES (:username, :hash)",
            username=user,
            hash=hash,
        )

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not request.form.get("shares").isdigit():
            return apology("must provide valid number of shares", 400)

        if int(request.form.get("shares")) < 1:
            return apology("must provide valid number of shares", 400)

        if int(request.form.get("shares")) != float(request.form.get("shares")):
            return apology("must provide valid number of shares", 400)

        unit_price = lookup(symbol)
        rows = db.execute(
            "SELECT * FROM portfolio WHERE userid = :id AND symbol = :symbol",
            id=session["user_id"],
            symbol=symbol,
        )

        # return apology if no symbol found
        if len(rows) != 1:
            return apology("must provide valid stock symbol", 400)

        if not shares:
            return apology("must provide number of shares", 400)

        # get shares already owned
        oldshares = rows[0]["shares"]

        shares = int(shares)

        if shares > oldshares:
            return apology("cannot sell more shares than you have", 400)

        # get current value of stock price times shares
        sold = unit_price["price"] * shares

        # add value of sold stocks to previous cash balance
        account_balance = db.execute(
            "SELECT cash FROM users WHERE id = :id", id=session["user_id"]
        )
        account_balance = account_balance[0]["cash"]
        account_balance = account_balance + sold

        # update cash balance in users table
        db.execute(
            "UPDATE users SET cash = :cash WHERE id = :id",
            cash=account_balance,
            id=session["user_id"],
        )

        # subtract sold shares from previous shares
        newshares = oldshares - shares

        # if shares remain, update portfolio table with new shares
        if shares > 0:
            db.execute(
                "UPDATE portfolio SET shares = :newshares WHERE userid = :id AND symbol = :symbol",
                newshares=newshares,
                id=session["user_id"],
                symbol=symbol,
            )

        # otherwise delete stock row because no shares remain
        else:
            db.execute(
                "DELETE FROM portfolio WHERE symbol = :symbol AND userid = :id",
                symbol=symbol,
                id=session["user_id"],
            )

        # update history table
        db.execute(
            "INSERT INTO history (userid, symbol, shares, method, price) VALUES (:userid, :symbol, :shares, 'Sell', :price)",
            userid=session["user_id"],
            symbol=symbol,
            shares=shares,
            price=unit_price["price"],
        )

        # redirect to index page
        return redirect("/")
    else:
        # get the user's current stocks
        portfolio = db.execute(
            "SELECT symbol FROM portfolio WHERE userid = :id", id=session["user_id"]
        )

        # render sell.html form, passing in current stocks
        return render_template("sell.html", portfolio=portfolio)
