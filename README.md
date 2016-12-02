# imapy
Python library to interact with email services using imap


## Usage

```python
>>> from imapy import Mailbox

>>> mailbox = Mailbox('some.email@outlook.com', 'secretpassword')
>>> mailbox.get_unread_emails()
[<IMAPyEmail Some important email - <email@microsoft.com>>,
 <IMAPyEmail Another Subject - <noreply@google.com>>]
>>>
```