import smtplib

login = {"email":"jayfishman98@gmail.com", "password":"Semasema3!"}

connection = smtplib.SMTP("smtp.gmail.com", 587)
connection.starttls()
connection.login(login.get("email"), login.get("password"))
connection.sendmail(login.get("email"), "deanmostafa7@gmail.com", "Sent from SMTPLib")





connection.close()