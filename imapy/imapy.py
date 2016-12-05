from __future__ import unicode_literals

import datetime
import imaplib
import smtplib
from email import message

from imapy.util import str_, message_parser


class Mailbox:
    def __init__(self, username, password, imap_server='imap-mail.outlook.com', smtp_server='smtp-mail.outlook.com',
                 smtp_port=587):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.imap = imaplib.IMAP4_SSL(imap_server)
        status, data = self.imap.login(username, self.password)
        if status == 'OK':
            print('imap login successful')
        self.select_folder('Inbox')

        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp = self._start_smtp()

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

    def send_email(self, to, subject, body):
        self._start_smtp()
        msg = ('''From: {email_from}\nSubject: {subject}\n\n{body}'''
               .format(email_from=self.username, to=to, subject=subject, body=body))
        return self.smtp.sendmail(self.username, to, msg)

    def _start_smtp(self):
        try:
            self.smtp.noop()
        except (smtplib.SMTPServerDisconnected, AttributeError):
            self.smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.smtp.starttls()
            self.smtp.login(self.username, self.password)
            return self.smtp

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
        self.email = message_parser(data)
        self.received_from = self.email['From']
        self.to = self.email['To']
        self.subject = self.email['Subject']
        self.date_received = datetime.datetime.strptime(self.email['Date'][:24], '%a, %d %b %Y %H:%M:%S')
        self.body = ''
        self.html = ''
        self.images = []
        self.process_email()

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
