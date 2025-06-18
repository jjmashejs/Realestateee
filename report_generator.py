import sqlite3
from datetime import datetime
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS issue_log (
        id INTEGER PRIMARY KEY,
        sender TEXT, subject TEXT, body TEXT,
        issue_type TEXT, urgency TEXT, timestamp DATETIME
    )''')
    conn.commit()
    conn.close()

def log_issue(sender, subject, body, issue_type, urgency):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO issue_log VALUES (NULL, ?, ?, ?, ?, ?, ?)",
              (sender, subject, body, issue_type, urgency, datetime.now()))
    conn.commit()
    conn.close()

def get_monthly_report():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT sender, issue_type, urgency, COUNT(*) FROM issue_log GROUP BY sender, issue_type, urgency")
    rows = c.fetchall()
    conn.close()
    report = ""
    for row in rows:
        report += f"{row[0]} - {row[1]} ({row[2]}): {row[3]}x\n"
    return report

def export_report_to_csv(filename='monthly_report.csv'):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT sender, subject, issue_type, urgency, timestamp FROM issue_log")
    rows = c.fetchall()
    conn.close()
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Sender", "Subject", "Issue", "Urgency", "Time"])
        writer.writerows(rows)

def export_report_to_pdf(filename='monthly_report.pdf'):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT sender, issue_type, urgency, COUNT(*) FROM issue_log GROUP BY sender, issue_type, urgency")
    rows = c.fetchall()
    conn.close()
    c = canvas.Canvas(filename, pagesize=letter)
    y = 750
    c.drawString(50, y, "Monthly Report")
    y -= 30
    for row in rows:
        c.drawString(50, y, f"{row[0]} - {row[1]} ({row[2]}): {row[3]}x")
        y -= 20
        if y < 40:
            c.showPage()
            y = 750
    c.save()