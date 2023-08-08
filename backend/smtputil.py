import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jinja2 import Environment, FileSystemLoader

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
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Noter email verification"
        msg["From"] = self.email
        msg["To"] = to

        text = "\r\n".join([
        "Hello,",
        "Please verify your email for Noter by clicking the link below.",
        "",
        link,
        "",
        "If you did not just create a Noter account, please ignore this email.",
        "Thank you,",
        "    the Noter Team",
        "https://getnoter.com"
        ])

        environment = Environment(loader=FileSystemLoader("backend/email_templates/"))
        html = environment.get_template("verifyemail.html.j2").render(link=link, autoescape=True)

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        try:
            self.connection.sendmail(self.email, to, msg.as_string())
            return True
        except: 
            return False
        
        
    def send_verification_code(self, to:str, code:str):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Noter verification code"
        msg["From"] = self.email
        msg["To"] = to

        text = "\r\n".join([
        "Hello,",
        "Your Noter verification code is:",
        "",
        code,
        "",
        "If you did not request this code, please change your account password immediately.",
        "Thank you,",
        "    the Noter Team",
        "https://getnoter.com"
        ])

        environment = Environment(loader=FileSystemLoader("backend/email_templates/"))
        html = environment.get_template("verifycode.html.j2").render(code=code, autoescape=True)

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        try:
            self.connection.sendmail(self.email, to, msg.as_string())
            return True
        except: return False

smtp_client = Client(
    os.environ['SMTP_SERVER'],
    int(os.environ['SMTP_PORT']),
    os.environ['SMTP_ADDRESS'],
    os.environ['SMTP_PASSWORD']
)
smtp_client.connect()