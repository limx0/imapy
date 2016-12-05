from __future__ import unicode_literals

import sys
import datetime
import imaplib
from email import message, message_from_string, message_from_bytes

from imapy.util import str_

PY3 = sys.version_info > (3, 0)


class Mailbox:
    def __init__(self, username, password, server='imap-mail.outlook.com'):
        self.imap = imaplib.IMAP4_SSL(server)
        self.login(username, password)
        self.select_folder('Inbox')

    def login(self, username, password):
        status, _ = self.imap.login(username, password)
        if status == 'OK':
            print("imapy login successful.")

    def select_folder(self, folder='Inbox'):
        self.imap.select(folder)

    def search_emails(self, unread=None, subject=None, received_from=None, date_from=None, date_to=None, body=None):
        args = []
        if unread is not None:
            args.append('UNSEEN' if unread else 'SEEN')
        if subject is not None:
            args.append('SUBJECT ' + subject)
        if received_from is not None:
            args.append('FROM ' + received_from)
        if date_from is not None:
            assert isinstance(date_from, (datetime.date, datetime.datetime))
            args.append('SENTSINCE ' + date_from.strftime('%d-%b-%Y'))
        if date_to is not None:
            assert isinstance(date_to, (datetime.date, datetime.datetime))
            args.append('SENTBEFORE ' + date_to.strftime('%d-%b-%Y'))
        if body is not None:
            args.append('BODY ' + body)
        return self._fetch(self._search(' '.join(args)))

    def get_unread_emails(self):
        return self.search_emails(unread=True)

    def _search(self, *args):
        status, data = self.imap.search(None, *args)
        if status != 'OK':
            raise Exception(status)
        if str_(data[0]) == '':
            return []
        return str(data[0], 'utf-8').split(' ')

    def _fetch(self, mail_id):
        if not mail_id:
            return []
        if isinstance(mail_id, (tuple, list)):
            mail_id = ','.join(mail_id)
        status, data = self.imap.fetch(mail_id, "(RFC822)")
        if status != 'OK':
            raise Exception(status)
        return [IMAPyEmail(d) for _, d in data[0::2]]


class IMAPyEmail(message.Message):
    def __init__(self, data):
        super().__init__()
        self.email = self.read_message(data)
        self.received_from = self.email['From']
        self.to = self.email['To']
        self.subject = self.email['Subject']
        self.date_received = datetime.datetime.strptime(self.email['Date'][:24], '%a, %d %b %Y %H:%M:%S')
        self.body = ''
        self.html = ''
        self.images = []
        self.process_email()

    @staticmethod
    def read_message(data):
        return message_from_bytes(data) if PY3 else message_from_string(data)

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