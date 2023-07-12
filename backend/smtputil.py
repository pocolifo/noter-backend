import smtplib

class Client:
    def __init__(self, server:str, port:int, email:str, password:str):
        self.server = server
        self.port = port
        self.email = email
        self.password = password
        self.connection = None
    
    def __del__(self):
        try: self.connection.close()
        except: pass

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