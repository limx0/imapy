
import sys
import imaplib
import email


class IMAPy:

    def __init__(self, username, password, server='imap-mail.outlook.com'):
        self.imap = imaplib.IMAP4_SSL(server)
        self.login(username, password)

        if sys.version_info > (3, 0):
            self.read_message = email.message_from_bytes
        else:
            self.read_message = email.message_from_string

    def login(self, username, password):
        status, _ = self.imap.login(username, password)
        if status == 'OK':
            print("Login Successful.")