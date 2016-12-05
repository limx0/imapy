# imapy
Python library to interact with email services using imap

[![Build Status](https://travis-ci.org/limx0/imapy.svg?branch=master)](https://travis-ci.org/limx0/imapy)

## Usage

#### Getting Started

```python
>>> from imapy import Mailbox
>>> mailbox = Mailbox('some.email@outlook.com', 'secretpassword')
```

#### Searching for emails
```python
>>> emails = mailbox.search_for_emails(
        unread=True,
        subject='Account',
        received_from='Microsoft',
        date_from=datetime.datetime(2016, 1, 1),
        date_to=datetime.datetime(2016, 1, 5),
        body='Your account upgrade',
    )

[<IMAPyEmail Account Update - <email@microsoft.com>>]

>>> mailbox.get_unread_emails()
[<IMAPyEmail Some important email - <email@microsoft.com>>,
 <IMAPyEmail Another Subject - <noreply@google.com>>]
>>>
```
