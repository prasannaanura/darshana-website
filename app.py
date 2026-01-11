from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecret123"


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/accomodation")
def accomodation():
    return render_template("accomodation.html")


@app.route("/service")
def service():
    return render_template("service.html")


@app.route("/reservation", methods=["GET", "POST"])
def reservation():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        checkin = request.form["checkin"]
        checkout = request.form["checkout"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO reservations (name, email, checkin, checkout) VALUES (?, ?, ?, ?)",
            (name, email, checkin, checkout)
        )
        conn.commit()
        conn.close()

        return f"Thank you {name}, your reservation is confirmed!"

    return render_template("reservation.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]

        if password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return "Wrong password"

    return render_template("admin_login.html")

@app.route("/admin")
def admin():
    # Check if admin is logged in
    if not session.get("admin"):
        return redirect(url_for("admin_login"))  # function name, no dash

    # Fetch reservations
    conn = get_db_connection()
    reservations = conn.execute("SELECT * FROM reservations").fetchall()
    conn.close()

    return render_template("admin.html", reservations=reservations)



@app.route("/delete/<int:id>", methods=["POST"])
def delete_reservation(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM reservations WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


@app.route("/review")
def review():
    return render_template("review.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)
