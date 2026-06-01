from datetime import date
import smtplib
import os


def main(all_jobs):
    text = ""

    for job in all_jobs:
        text += f"Title: {job[0]}\nCompany: {job[1]}\nJob: {job[2]}\nSalary: {job[3]}\nLocation: {job[4]}\n\n"

    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        today = date.today()
        formatted_date = today.strftime("%d/%m/%Y")
        msg = MIMEMultipart()
        msg['Subject'] = f"Job Listings on {formatted_date}"
        msg['From'] = "alifazalansari00@gmail.com"
        msg['To'] = "alifazalansari00@gmail.com"

        # Attach the body with explicit UTF-8 encoding
        msg.attach(MIMEText(text, 'plain', 'utf-8'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_TEMP_PWD"))

        # Pass the message as a string via as_string()
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
    except:
        raise Exception
