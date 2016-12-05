
import unittest

from getpass import getpass, getuser
from imapy.imapy import Mailbox


class IMAPyTest(unittest.TestCase):
    def test(self):
        m = Mailbox(getuser(), getpass())
        assert(m)