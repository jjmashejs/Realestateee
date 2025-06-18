from flask import Flask, render_template, request, redirect, session, send_file
from auth import authenticate
from email_handler import fetch_emails
from nlp_classifier import classify_issue
from dispatcher import handle_dispatch
from report_generator import log_issue, get_monthly_report, export_report_to_csv, export_report_to_pdf
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # Replace with env var in prod

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        if authenticate(user, pwd):
            session["user"] = user
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    emails = fetch_emails()
    issues = []
    for e in emails:
        issue, urgency = classify_issue(e["body"])
        result = handle_dispatch(issue, urgency)
        log_issue(e["from"], e["subject"], e["body"], issue, urgency)
        issues.append({
            "from": e["from"],
            "subject": e["subject"],
            "issue": issue,
            "urgency": urgency,
            "result": result
        })
    return render_template("dashboard.html", issues=issues)

@app.route("/reports")
def reports():
    if "user" not in session:
        return redirect("/")
    report_text = get_monthly_report()
    return render_template("reports.html", report=report_text)

@app.route("/export/<format>")
def export(format):
    if format == "csv":
        export_report_to_csv()
        return send_file("monthly_report.csv", as_attachment=True)
    elif format == "pdf":
        export_report_to_pdf()
        return send_file("monthly_report.pdf", as_attachment=True)
    return "Invalid format", 400

if __name__ == "__main__":
    from report_generator import init_db
    init_db()
    app.run(debug=True)