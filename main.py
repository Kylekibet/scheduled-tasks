import random
import smtplib
import pandas as pd
import datetime as dt
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
GMAIL_SMTP_SERVER = "smtp.gmail.com"

def send_email(receiver, msg):
    with smtplib.SMTP_SSL(GMAIL_SMTP_SERVER, 465) as connection:
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(MY_EMAIL, receiver, msg)

def generate_letter(name, receiver):
    letters = ['letter_1.txt', 'letter_2.txt', 'letter_3.txt']
    letter = random.choice(letters)
    try:
        with open(f"letter_templates/{letter}") as f:
            letter = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"letter_templates/{letter} not found")
    else:
        letter = letter.replace("[NAME]", f"{name}")
        msg_body = (
            f"From: {MY_EMAIL}\r\n"
            f"To: {receiver}\r\n"
            "MIME-Version: 1.0\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            f"Subject: Happy Birthday\r\n"
            "\r\n"
            f"{letter}!!!"
        )
    return msg_body

try:
    with open("birthdays.csv") as data_file:
        birthdays = pd.read_csv(data_file)
except FileNotFoundError:
    print("No birthdays.csv found")
else:
    birthdays = birthdays.to_dict(orient="records")
    now = dt.datetime.now()

    for birthday in birthdays:
        if now.day == birthday["day"] and now.month == birthday["month"]:
            message = generate_letter(birthday["name"], birthday["email"])
            send_email(birthday["email"], message)