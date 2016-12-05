
import os
import sys
from email import message_from_string, message_from_bytes

TEST_ACCOUNT = os.environ['IMAPY_TEST_ACCOUNT']
TEST_PW = os.environ['IMAPY_TEST_PW']
PY3 = sys.version_info > (3, 0)


def message_parser(data):
    if PY3:
        return message_from_bytes(data)
    else:
        return message_from_string(data)


def str_(s):
    return str(s, 'utf-8')
