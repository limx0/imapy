
import sys
import imaplib
import email

PY3 = sys.version_info > (3, 0)


class Mailbox:
    def __init__(self, username, password, server='imap-mail.outlook.com'):
        self.imap = imaplib.IMAP4_SSL(server)
        self.imap.login(username, password)
        self.split_char = b' ' if PY3 else ' '

    def login(self, username, password):
        status, _ = self.imap.login(username, password)
        if status == 'OK':
            print("Login Successful.")

    def select_folder(self, folder='Inbox'):
        self.imap.select(folder)

    def search_emails(self, unread=None, subject=None, received_from=None,
                      date_from=None, date_to=None):
        raise NotImplementedError()

    def get_unread_emails(self):
        return self._search('UNSEEN')

    def _search(self, *args):
        status, data = self.imap.search(None, *args)
        if status != 'OK':
            raise Exception(status)
        return data[0].split(self.split_char)

    def _fetch(self, mail_id):
        if isinstance(mail_id, (tuple, list)):
            mail_id = ','.join(mail_id)
        status, data = self.imap.fetch(mail_id, "(RFC822)")
        if status != 'OK':
            raise Exception(status)
        return [IMAPyEmail(d) for _, d in data[0::2]]


class IMAPyEmail(email.message.Message):
    def __init__(self, data):
        self.email = self.read_message(data)
        self.received_from = self.email['From']
        self.to = self.email['To']
        self.subject = self.email['Subject']
        self.date = self.email['Date']
        self.body = ''
        self.html = ''
        self.images = []
        self.process_email()

    @staticmethod
    def read_message(data):
        if PY3:
            return email.message_from_bytes(data)
        else:
            return email.message_from_string(data)

    def process_email(self):
        if self.email.get_content_maintype() == 'multipart':
            for part in self.email.get_payload():
                if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'html':
                    self.html = part.get_payload()
                elif part.get_content_maintype() == 'image':
                    self.images.append(part.get_payload())
        elif self.email.get_content_maintype() == 'text':
            self.body = self.email.get_payload()

    def __repr__(self):
        return ('<IMAPyEmail {subject} - {rec_from}>'
                .format(rec_from=self.received_from, subject=self.subject))