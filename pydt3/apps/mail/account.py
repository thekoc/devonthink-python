from __future__ import annotations
from ...helper_bridging import OSAObjProxy, OSAObjArray
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .mailbox import Mailbox



class Account(OSAObjProxy):
    """A Mail account for receiving messages (POP/IMAP)."""

    # ========== Elements ==========
    @property
    def mailboxes(self) -> OSAObjArray[Mailbox]:
        """Mailboxes contained by this account."""
        return self._get_property('mailboxes')

    # ========== Properties ==========
    @property
    def delivery_account(self) -> Optional[SmtpServer]:
        """The delivery account used when sending mail from this account."""
        return self._get_property('deliveryAccount')

    @property
    def name(self) -> str:
        """The name of an account."""
        return self._get_property('name')

    @property
    def id(self) -> str:
        """The unique identifier of the account."""
        return self._get_property('id', read_only=True)

    @property
    def password(self) -> str:
        """Password for this account."""
        return self._get_property('password')

    @password.setter
    def password(self, value: str):
        self._set_property('password', value)

    @property
    def authentication(self) -> str:
        """Preferred authentication scheme for account."""
        return self._get_property('authentication')

    @authentication.setter
    def authentication(self, value: str):
        self._set_property('authentication', value)

    @property
    def account_type(self) -> str:
        """The type of an account."""
        return self._get_property('accountType', read_only=True)

    @property
    def email_addresses(self) -> OSAObjArray[str]:
        """The list of email addresses configured for an account."""
        return self._get_property('emailAddresses')

    @property
    def full_name(self) -> str:
        """The user's full name configured for an account."""
        return self._get_property('fullName')

    @full_name.setter
    def full_name(self, value: str):
        self._set_property('fullName', value)

    @property
    def empty_junk_messages_frequency(self) -> int:
        """Number of days before junk messages are deleted."""
        return self._get_property('emptyJunkMessagesFrequency')

    @empty_junk_messages_frequency.setter
    def empty_junk_messages_frequency(self, value: int):
        self._set_property('emptyJunkMessagesFrequency', value)

    @property
    def empty_trash_frequency(self) -> int:
        """Number of days before messages in the trash are permanently deleted."""
        return self._get_property('emptyTrashFrequency')

    @empty_trash_frequency.setter
    def empty_trash_frequency(self, value: int):
        self._set_property('emptyTrashFrequency', value)

    @property
    def empty_junk_messages_on_quit(self) -> bool:
        """Indicates whether junk messages are deleted on quit."""
        return self._get_property('emptyJunkMessagesOnQuit')

    @empty_junk_messages_on_quit.setter
    def empty_junk_messages_on_quit(self, value: bool):
        self._set_property('emptyJunkMessagesOnQuit', value)

    @property
    def empty_trash_on_quit(self) -> bool:
        """Indicates whether trash messages are permanently deleted on quit."""
        return self._get_property('emptyTrashOnQuit')

    @empty_trash_on_quit.setter
    def empty_trash_on_quit(self, value: bool):
        self._set_property('emptyTrashOnQuit', value)

    @property
    def enabled(self) -> bool:
        """Indicates whether the account is enabled."""
        return self._get_property('enabled')

    @enabled.setter
    def enabled(self, value: bool):
        self._set_property('enabled', value)

    @property
    def user_name(self) -> str:
        """The user name used to connect to an account."""
        return self._get_property('userName')

    @user_name.setter
    def user_name(self, value: str):
        self._set_property('userName', value)

    @property
    def account_directory(self) -> str:
        """The directory where the account stores things on disk."""
        return self._get_property('accountDirectory', read_only=True)

    @property
    def port(self) -> int:
        """The port used to connect to an account."""
        return self._get_property('port')

    @port.setter
    def port(self, value: int):
        self._set_property('port', value)

    @property
    def server_name(self) -> str:
        """The host name used to connect to an account."""
        return self._get_property('serverName')

    @server_name.setter
    def server_name(self, value: str):
        self._set_property('serverName', value)

    @property
    def move_deleted_messages_to_trash(self) -> bool:
        """Indicates whether deleted messages are moved to the trash."""
        return self._get_property('moveDeletedMessagesToTrash')

    @move_deleted_messages_to_trash.setter
    def move_deleted_messages_to_trash(self, value: bool):
        self._set_property('moveDeletedMessagesToTrash', value)

    @property
    def uses_ssl(self) -> bool:
        """Indicates whether SSL is enabled for this receiving account."""
        return self._get_property('usesSsl')

    @uses_ssl.setter
    def uses_ssl(self, value: bool):
        self._set_property('usesSsl', value)
