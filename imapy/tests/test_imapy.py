

import unittest
import datetime
import time

from imapy.imapy import Mailbox
from imapy.util import TEST_ACCOUNT, TEST_PW


class TestLogin(unittest.TestCase):
    mailbox = Mailbox(TEST_ACCOUNT, TEST_PW)


class IMAPyTest(TestLogin):

    def test_search_unread(self):
        assert self.mailbox.search_emails(unread=False)

    def test_search_subject(self):
        assert self.mailbox.search_emails(subject='test')

    def test_search_received_from(self):
        assert self.mailbox.search_emails(received_from=TEST_ACCOUNT)

    def test_search_date_from(self):
        assert self.mailbox.search_emails(date_from=datetime.datetime(2016, 12, 4))

    def test_search_date_to(self):
        assert self.mailbox.search_emails(date_to=datetime.datetime(2016, 12, 7))

    def test_search_body(self):
        assert self.mailbox.search_emails(body='hello')

    def test_search_date_from_false(self):
        with self.assertRaises(AssertionError):
            self.mailbox.search_emails(date_from='20160101')

    def test_send_email(self):
        assert self.mailbox.send_email(TEST_ACCOUNT, 'TEST_SUBJECT', 'TEST_BODY') == {}
        time.sleep(10)
        assert self.mailbox.search_emails(subject='TEST_SUBJECT', body='TEST_BODY')


if __name__ == '__main__':
    unittest.main()
