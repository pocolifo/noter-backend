import os
import smtplib

class Client:
    def __init__(self, server:str, port:int, email:str, password:str):
        self.server = server
        self.port = port
        self.email = email
        self.password = password
        self.connection = None
    
    def __del__(self):
        self.connection.close()

    def connect(self):
        try:
            self.connection = smtplib.SMTP(self.server, self.port) # gmail: smtp.gmail.com:587
            self.connection.starttls() # gmail requirement
            self.connection.ehlo() # gmail requirement 
            self.connection.login(self.email, self.password)
            return True
        except Exception: return False
        
        
    def send_verification_email(self, to:str, link:str):
        msg = "\r\n".join([
          "From: {0}".format(self.email),
          "To: {0}".format(to),
          "Subject: Verify Your Email!",
          "",
          "Click this link to verify: {0}".format(link)
          ])
        try:
            self.connection.sendmail(self.email, to, msg)
            return True
        except: return False
        
        
    def send_verification_code(self, to:str, code:str):
        msg = "\r\n".join([
          "From: {0}".format(self.email),
          "To: {0}".format(to),
          "Subject: Verification Code",
          "",
          "Your verification code: {0}".format(code)
          ])
        try:
            self.connection.sendmail(self.email, to, msg)
            return True
        except: return False

smtp_client = Client(
    os.environ['SMTP_SERVER'],
    int(os.environ['SMTP_PORT']),
    os.environ['SMTP_ADDRESS'],
    os.environ['SMTP_PASSWORD']
)
smtp_client.connect()