import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

from config import settings as config


class EmailClient():
    """ Connects to email servers and sends out notification emails """

    def __init__(self):
        self.password = config["email"]["password"]
        self.from_address = config["email"]["from_address"]

    def notify_run_complete(self, to_address, file_name=""):
        """
        Sends an email notification for end of optimization run.
        Args:
            to_address: email address for recipient.
            file_name: fully qualified file name for attachment. Optional.
        """
        msg = MIMEMultipart()

        msg['From'] = self.from_address
        msg['To'] = to_address
        msg['Subject'] = "ProbSyllabifier AWS run"
        body =  '''
                Run complete.
                Turn off server at: https://guseas.signin.aws.amazon.com/console
                '''
        msg.attach(MIMEText(body, 'plain'))

        if(file_name != ''):
            attachment = open(file_name, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % file_name.split('/')[-1])
            msg.attach(part)

        server = smtplib.SMTP(config["email"]["smtp_server"], config["email"]["smtp_port"])
        server.starttls()
        server.login(self.from_address, self.password)
        text = msg.as_string()
        server.sendmail(self.from_address, to_address, text)
        server.quit()
