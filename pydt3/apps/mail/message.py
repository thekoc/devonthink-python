from __future__ import annotations
from ...helper_bridging import OSAObjProxy, OSAObjArray


class Message(OSAObjProxy):
    """An email message."""

    # ========== Elements ==========
    @property
    def bcc_recipients(self) -> OSAObjArray[Recipient]:
        """Returns the BCC recipients of the message."""
        return self._get_property('bccRecipients')
    
    @property
    def cc_recipients(self) -> OSAObjArray[Recipient]:
        """Returns the CC recipients of the message."""
        return self._get_property('ccRecipients')

    @property
    def recipients(self) -> OSAObjArray[Recipient]:
        """Returns all the recipients of the message."""
        return self._get_property('recipients')

    @property
    def to_recipients(self) -> OSAObjArray[Recipient]:
        """Returns the TO recipients of the message."""
        return self._get_property('toRecipients')

    @property
    def headers(self) -> OSAObjArray[Header]:
        """Returns the headers of the message."""
        return self._get_property('headers')

    @property
    def mail_attachments(self) -> OSAObjArray[MailAttachment]:
        """Returns the mail attachments of the message."""
        return self._get_property('mailAttachments')

    # ========== Properties ==========
    @property
    def id(self) -> int:
        """The unique identifier of the message."""
        return self._get_property('id')

    @property
    def all_headers(self) -> str:
        """All the headers of the message."""
        return self._get_property('allHeaders')

    @property
    def background_color(self) -> str:
        """The background color of the message."""
        return self._get_property('backgroundColor')

    @background_color.setter
    def background_color(self, value: str):
        """Set the background color of the message."""
        self._set_property('backgroundColor', value)

    @property
    def mailbox(self) -> Mailbox:
        """The mailbox in which this message is filed."""
        return self._get_property('mailbox')

    @mailbox.setter
    def mailbox(self, value: Mailbox):
        """Set the mailbox in which this message is filed."""
        self._set_property('mailbox', value)

    @property
    def content(self) -> str:
        """Contents of an email message."""
        return self._get_property('content')

    @property
    def date_received(self) -> datetime:
        """The date a message was received."""
        return self._get_property('dateReceived')

    @property
    def date_sent(self) -> datetime:
        """The date a message was sent."""
        return self._get_property('dateSent')

    @property
    def deleted_status(self) -> bool:
        """Indicates whether the message is deleted or not."""
        return self._get_property('deletedStatus')

    @deleted_status.setter
    def deleted_status(self, value: bool):
        """Set the deleted status of the message."""
        self._set_property('deletedStatus', value)

    @property
    def flagged_status(self) -> bool:
        """Indicates whether the message is flagged or not."""
        return self._get_property('flaggedStatus')

    @flagged_status.setter
    def flagged_status(self, value: bool):
        """Set the flagged status of the message."""
        self._set_property('flaggedStatus', value)

    @property
    def flag_index(self) -> int:
        """The flag on the message, or -1 if the message is not flagged."""
        return self._get_property('flagIndex')

    @flag_index.setter
    def flag_index(self, value: int):
        """Set the flag index of the message."""
        self._set_property('flagIndex', value)

    @property
    def junk_mail_status(self) -> bool:
        """Indicates whether the message has been marked junk or evaluated to be junk by the junk mail filter."""
        return self._get_property('junkMailStatus')

    @junk_mail_status.setter
    def junk_mail_status(self, value: bool):
        """Set the junk mail status of the message."""
        self._set_property('junkMailStatus', value)

    @property
    def read_status(self) -> bool:
        """Indicates whether the message is read or not."""
        return self._get_property('readStatus')

    @read_status.setter
    def read_status(self, value: bool):
        """Set the read status of the message."""
        self._set_property('readStatus', value)

    @property
    def message_id(self) -> str:
        """The unique message ID string."""
        return self._get_property('messageId')

    @property
    def source(self) -> str:
        """Raw source of the message."""
        return self._get_property('source')

    @property
    def reply_to(self) -> str:
        """The address that replies should besent to."""
        return self._get_property('replyTo')

    @property
    def message_size(self) -> int:
        """The size (in bytes) of a message."""
        return self._get_property('messageSize')

    @property
    def sender(self) -> str:
        """The sender of the message."""
        return self._get_property('sender')

    @property
    def subject(self) -> str:
        """The subject of the message."""
        return self._get_property('subject')

    @property
    def was_forwarded(self) -> bool:
        """Indicates whether the message was forwarded or not."""
        return self._get_property('wasForwarded')

    @property
    def was_redirected(self) -> bool:
        """Indicates whether the message was redirected or not."""
        return self._get_property('wasRedirected')

    @property
    def was_replied_to(self) -> bool:
        """Indicates whether the message was replied to or not."""
        return self._get_property('wasRepliedTo')
    