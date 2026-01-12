from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecret123"

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'prasannaanura1970@gmail.com'  # Your Gmail
app.config['MAIL_PASSWORD'] = 'pvithjbtpybxatkb'              # App Password (remove spaces)
app.config['MAIL_DEFAULT_SENDER'] = 'prasannaanura1970@gmail.com'

mail = Mail(app)


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def send_booking_notification(name, email, checkin, checkout):
    """Send email notification to admin when new booking is made"""
    try:
        msg = Message(
            subject='🏨 New Booking - StayEasy',
            recipients=['prasannaanura1970@gmail.com']  # CHANGED: Admin email receives notification
        )
        
        # HTML email body
        msg.html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #2c7a7b; border-bottom: 3px solid #2c7a7b; padding-bottom: 10px;">
                    New Booking Received!
                </h2>
                
                <div style="margin: 20px 0;">
                    <h3 style="color: #333;">Guest Details:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd; font-weight: bold;">Name:</td>
                            <td style="padding: 10px; border: 1px solid #ddd;">{name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd; font-weight: bold;">Email:</td>
                            <td style="padding: 10px; border: 1px solid #ddd;">{email}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd; font-weight: bold;">Check-in:</td>
                            <td style="padding: 10px; border: 1px solid #ddd;">{checkin}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd; font-weight: bold;">Check-out:</td>
                            <td style="padding: 10px; border: 1px solid #ddd;">{checkout}</td>
                        </tr>
                    </table>
                </div>
                
                <p style="color: #666; margin-top: 20px;">
                    Please check your admin panel for more details and to manage this booking.
                </p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #999; font-size: 12px;">
                    <p>StayEasy Hotel Management System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version (fallback)
        msg.body = f"""
New Booking Received - StayEasy

Guest Details:
--------------
Name: {name}
Email: {email}
Check-in: {checkin}
Check-out: {checkout}

Please check the admin panel for more details.

---
StayEasy Hotel Management System
        """
        
        mail.send(msg)
        print("✅ Email notification sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False


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
        print("🔵 POST request received")  # Debug 1
        
        name = request.form["name"]
        email = request.form["email"]
        checkin = request.form["checkin"]
        checkout = request.form["checkout"]

        print(f"📝 Booking data: {name}, {email}, {checkin}, {checkout}")  # Debug 2

        # Save to database
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO reservations (name, email, checkin, checkout) VALUES (?, ?, ?, ?)",
            (name, email, checkin, checkout)
        )
        conn.commit()
        conn.close()

        print("💾 Database save complete")  # Debug 3

        # Send email notification to admin
        print("📧 Attempting to send email...")  # Debug 4
        result = send_booking_notification(name, email, checkin, checkout)
        print(f"📧 Email result: {result}")  # Debug 5

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
        return redirect(url_for("admin_login"))

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