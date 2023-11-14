
from __future__ import annotations

from typing import TYPE_CHECKING

from ...helper_bridging import OSAObjProxy, OSAObjArray

if TYPE_CHECKING:
    from .message import Message
    from .account import Account


class Mailbox(OSAObjProxy):
    """A mailbox that holds messages."""

    # ========== Elements ==========
    @property
    def mailboxes(self) -> OSAObjArray[Mailbox]:
        """Returns the mailboxes contained in this mailbox."""
        return self._get_property('mailboxes')
    
    @property
    def messages(self) -> OSAObjArray[Message]:
        """Returns the messages contained in this mailbox."""
        return self._get_property('messages')
    
    # ========== Properties ==========
    @property
    def name(self) -> str:
        """The name of a mailbox."""
        return self._get_property('name')
    
    @name.setter
    def name(self, value: str):
        """Set the name of a mailbox."""
        self._set_property('name', value)

    @property
    def unread_count(self) -> int:
        """The number of unread messages in the mailbox."""
        return self._get_property('unreadCount')
    
    @property
    def account(self) -> Account:
        """The account that the mailbox belongs to."""
        return self._get_property('account')

    @property
    def container(self) -> Mailbox:
        """The mailbox that contains this mailbox."""
        return self._get_property('container')