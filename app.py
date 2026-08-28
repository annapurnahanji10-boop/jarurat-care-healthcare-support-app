from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "jarurat_care.db"


# =========================================================
# DATABASE
# =========================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS support_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            issue TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# PATIENT SUPPORT PAGE
# =========================================================

@app.route("/support", methods=["GET"])
def support():
    return render_template("support.html")


# =========================================================
# SUBMIT PATIENT SUPPORT REQUEST
# =========================================================

@app.route("/submit-support", methods=["POST"])
def submit_support():

    try:
        # Get data from form
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        phone = request.form.get("phone", "").strip()
        location = request.form.get("location", "").strip()
        issue = request.form.get("issue", "").strip()

        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        if not name:
            return render_template(
                "support.html",
                error="Please enter your full name."
            )

        if not age:
            return render_template(
                "support.html",
                error="Please enter your age."
            )

        if not phone:
            return render_template(
                "support.html",
                error="Please enter your phone number."
            )

        if not location:
            return render_template(
                "support.html",
                error="Please enter your location."
            )

        if not issue:
            return render_template(
                "support.html",
                error="Please describe how we can help."
            )

        # -----------------------------------------
        # AGE VALIDATION
        # -----------------------------------------

        try:
            age = int(age)
        except ValueError:
            return render_template(
                "support.html",
                error="Age must be a valid number."
            )

        if age < 1 or age > 120:
            return render_template(
                "support.html",
                error="Age must be between 1 and 120."
            )

        # -----------------------------------------
        # PHONE VALIDATION
        # -----------------------------------------

        phone_digits = phone.replace(" ", "").replace("-", "")

        if not phone_digits.isdigit() or len(phone_digits) < 10:
            return render_template(
                "support.html",
                error="Please enter a valid phone number."
            )

        # -----------------------------------------
        # MAKE SURE DATABASE EXISTS
        # -----------------------------------------

        init_db()

        # -----------------------------------------
        # SAVE REQUEST
        # -----------------------------------------

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO support_requests
            (
                name,
                age,
                phone,
                location,
                issue,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            age,
            phone,
            location,
            issue,
            datetime.now().strftime("%d-%m-%Y %H:%M")
        ))

        conn.commit()
        conn.close()

        # -----------------------------------------
        # REDIRECT TO SUCCESS PAGE
        # -----------------------------------------

        return redirect(
            url_for("success", name=name)
        )

    except Exception as e:

        print("PATIENT SUPPORT ERROR:", repr(e))

        return render_template(
            "support.html",
            error="Unable to save your request. Please try again."
        )


# =========================================================
# SUCCESS PAGE
# =========================================================

@app.route("/success")
def success():

    name = request.args.get("name", "Patient")

    return render_template(
        "success.html",
        name=name
    )


# =========================================================
# AI FAQ ASSISTANT PAGE
# =========================================================

@app.route("/chatbot", methods=["GET"])
def chatbot():

    return render_template("chatbot.html")


# =========================================================
# AI FAQ ASSISTANT
# =========================================================

@app.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json(silent=True) or {}

        question = data.get("question", "").strip().lower()

        if not question:

            return jsonify({
                "response":
                "Please type a healthcare-support question."
            })


        # -----------------------------------------
        # GREETING
        # -----------------------------------------

        if any(word in question for word in [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]):

            answer = """
👋 Hello!

Welcome to Jarurat Care.

I'm your healthcare-support assistant.

I can help with:

🏥 Healthcare support
👨‍⚕️ Doctor appointments
🚨 Emergency guidance
💊 Medicine information
📝 Patient support requests

How can I help you today?
"""


        # -----------------------------------------
        # DOCTOR APPOINTMENT
        # -----------------------------------------

        elif (
            ("doctor" in question or "physician" in question)
            and any(word in question for word in [
                "appointment",
                "book",
                "booking",
                "consult",
                "visit"
            ])
        ):

            answer = """
👨‍⚕️ Doctor Appointment

To make a doctor appointment, contact a nearby
hospital or clinic or use the healthcare provider's
official appointment system.

Keep your preferred date and time ready when booking.

You can also submit a Patient Support Request
through Jarurat Care if you need general support.
"""


        # -----------------------------------------
        # EMERGENCY
        # -----------------------------------------

        elif any(word in question for word in [
            "emergency",
            "urgent",
            "critical",
            "life threatening",
            "life-threatening"
        ]):

            answer = """
🚨 Emergency Guidance

If you are experiencing a serious or life-threatening
emergency, contact your local emergency medical service
or go to the nearest emergency department immediately.

Jarurat Care provides general information and is not
a replacement for emergency medical care.
"""


        # -----------------------------------------
        # HEALTHCARE SUPPORT
        # -----------------------------------------

        elif any(phrase in question for phrase in [
            "healthcare support",
            "health care support",
            "health support",
            "medical support",
            "get support",
            "need support",
            "health help",
            "medical help"
        ]):

            answer = """
🏥 Healthcare Support

You can get healthcare support by contacting a nearby
hospital, clinic, qualified healthcare professional,
or trusted healthcare-support organization.

You can also submit a Patient Support Request through
the Jarurat Care support page.

Your request can then be reviewed by the support team.
"""


        # -----------------------------------------
        # PATIENT SUPPORT
        # -----------------------------------------

        elif any(phrase in question for phrase in [
            "patient support",
            "support request",
            "submit request",
            "support form",
            "register",
            "registration"
        ]):

            answer = """
📝 Patient Support Request

You can submit a request through the Patient Support page.

The form collects:

• Full name
• Age
• Phone number
• Location
• Support requirement

After submission, the request is stored in the
Jarurat Care database for support-team review.
"""


        # -----------------------------------------
        # MEDICINE
        # -----------------------------------------

        elif any(word in question for word in [
            "medicine",
            "medicines",
            "medication",
            "tablet",
            "tablets",
            "drug",
            "drugs",
            "dosage"
        ]):

            answer = """
💊 Medicine Information

For medicine-related questions, please consult
a qualified doctor or pharmacist.

The appropriate medicine and dosage depend on
the individual's condition and medical history.

Do not start, stop, or change prescription medicines
without professional medical advice.
"""


        # -----------------------------------------
        # SYMPTOMS
        # -----------------------------------------

        elif any(word in question for word in [
            "symptom",
            "symptoms",
            "fever",
            "cough",
            "headache",
            "pain",
            "cold",
            "vomiting"
        ]):

            answer = """
🩺 General Symptom Guidance

Symptoms can have many possible causes.

If symptoms are severe, persistent, or concerning,
please consult a qualified healthcare professional.

This assistant cannot diagnose medical conditions.
"""


        # -----------------------------------------
        # HOSPITAL / CLINIC
        # -----------------------------------------

        elif any(word in question for word in [
            "hospital",
            "clinic",
            "health center",
            "health centre"
        ]):

            answer = """
🏥 Finding Healthcare Facilities

You can look for a nearby hospital, clinic, or
qualified healthcare provider based on your location.

For urgent situations, choose the nearest appropriate
emergency medical facility.
"""


        # -----------------------------------------
        # PRIVACY
        # -----------------------------------------

        elif any(word in question for word in [
            "privacy",
            "private",
            "personal information",
            "personal data"
        ]):

            answer = """
🔒 Privacy

Please avoid sharing highly sensitive personal or
medical information with the FAQ Assistant.

Only provide information necessary for your support
request.
"""


        # -----------------------------------------
        # THANK YOU
        # -----------------------------------------

        elif any(word in question for word in [
            "thank you",
            "thanks",
            "thank"
        ]):

            answer = """
💙 You're welcome!

Jarurat Care is here to make healthcare-support
information easier to access.

Stay safe and take care!
"""


        # -----------------------------------------
        # DEFAULT
        # -----------------------------------------

        else:

            answer = """
🤖 I can help with general healthcare-support questions.

Try asking:

🏥 How can I get healthcare support?

👨‍⚕️ How can I make a doctor appointment?

🚨 What should I do in an emergency?

💊 Can I get information about medicines?

📝 How can I submit a patient support request?

🩺 What should I do about my symptoms?
"""


        return jsonify({
            "response": answer.strip()
        })


    except Exception as e:

        print("FAQ ERROR:", repr(e))

        return jsonify({
            "response":
            "Sorry, something went wrong while processing your question."
        }), 500


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin", methods=["GET"])
def admin():

    init_db()

    conn = get_db_connection()

    requests = conn.execute("""
        SELECT *
        FROM support_requests
        ORDER BY id DESC
    """).fetchall()

    total_requests = conn.execute("""
        SELECT COUNT(*) AS count
        FROM support_requests
    """).fetchone()["count"]

    conn.close()

    return render_template(
        "admin.html",
        requests=requests,
        total_requests=total_requests
    )


# =========================================================
# DELETE SUPPORT REQUEST
# =========================================================

@app.route(
    "/delete-request/<int:request_id>",
    methods=["POST"]
)
def delete_request(request_id):

    conn = get_db_connection()

    conn.execute("""
        DELETE FROM support_requests
        WHERE id = ?
    """, (request_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )