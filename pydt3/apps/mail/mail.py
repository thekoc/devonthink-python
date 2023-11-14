from __future__ import annotations

from typing import TYPE_CHECKING

from ...helper_bridging import OSAObjArray, Application

if TYPE_CHECKING:
    from .account import Account, POPAccount, IMAPAccount, ICloudAccount
    from .smtp_server import SMTPServer
    from .message import Message
    from .mailbox import Mailbox
    from .message_viewer import MessageViewer
    from .rule import Rule
    from .signature import Signature


class Mail(Application):
    """Mail's top level scripting object."""

    # ========== Elements ==========
    @property
    def accounts(self) -> OSAObjArray[Account]:
        return self._get_property('accounts')

    @property
    def pop_accounts(self) -> OSAObjArray[POPAccount]:
        return self._get_property('popAccounts')

    @property
    def imap_accounts(self) -> OSAObjArray[IMAPAccount]:
        return self._get_property('imapAccounts')

    @property
    def icloud_accounts(self) -> OSAObjArray[ICloudAccount]:
        return self._get_property('icloudAccounts')

    @property
    def smtp_servers(self) -> OSAObjArray[SMTPServer]:
        return self._get_property('smtpServers')

    @property
    def outgoing_messages(self) -> OSAObjArray[Message]:
        return self._get_property('outgoingMessages')

    @property
    def mailboxes(self) -> OSAObjArray[Mailbox]:
        return self._get_property('mailboxes')

    @property
    def message_viewers(self) -> OSAObjArray[MessageViewer]:
        return self._get_property('messageViewers')

    @property
    def rules(self) -> OSAObjArray[Rule]:
        return self._get_property('rules')

    @property
    def signatures(self) -> OSAObjArray[Signature]:
        return self._get_property('signatures')

    # ========== Properties ==========
    @property
    def always_bcc_myself(self) -> bool:
        return self._get_property('alwaysBccMyself')

    @always_bcc_myself.setter
    def always_bcc_myself(self, value: bool):
        self._set_property('alwaysBccMyself', value)

    @property
    def always_cc_myself(self) -> bool:
        return self._get_property('alwaysCcMyself')

    @always_cc_myself.setter
    def always_cc_myself(self, value: bool):
        self._set_property('alwaysCcMyself', value)

    @property
    def selection(self) -> list:
        """List of messages that the user has selected."""
        return self._get_property('selection')

    @property
    def application_version(self) -> str:
        """The build number of the application."""
        return self._get_property('applicationVersion')

    @property
    def fetch_interval(self) -> int:
        """The interval (in minutes) between automatic fetches of new mail."""
        return self._get_property('fetchInterval')

    @fetch_interval.setter
    def fetch_interval(self, value: int):
        self._set_property('fetchInterval', value)

    @property
    def background_activity_count(self) -> int:
        """Number of background activities currently running in Mail."""
        return self._get_property('backgroundActivityCount')

    # Continuation of Application Properties
    @property
    def choose_signature_when_composing(self) -> bool:
        return self._get_property('chooseSignatureWhenComposing')

    @choose_signature_when_composing.setter
    def choose_signature_when_composing(self, value: bool):
        self._set_property('chooseSignatureWhenComposing', value)

    @property
    def color_quoted_text(self) -> bool:
        return self._get_property('colorQuotedText')

    @color_quoted_text.setter
    def color_quoted_text(self, value: bool):
        self._set_property('colorQuotedText', value)

    @property
    def default_message_format(self) -> str:
        return self._get_property('defaultMessageFormat')

    @default_message_format.setter
    def default_message_format(self, value: str):
        self._set_property('defaultMessageFormat', value)

    @property
    def download_html_attachments(self) -> bool:
        return self._get_property('downloadHtmlAttachments')

    @download_html_attachments.setter
    def download_html_attachments(self, value: bool):
        self._set_property('downloadHtmlAttachments', value)

    @property
    def drafts_mailbox(self) -> Mailbox:
        """The top level Drafts mailbox."""
        return self._get_property('draftsMailbox')

    @property
    def expand_group_addresses(self) -> bool:
        return self._get_property('expandGroupAddresses')

    @expand_group_addresses.setter
    def expand_group_addresses(self, value: bool):
        self._set_property('expandGroupAddresses', value)

    @property
    def fixed_width_font(self) -> str:
        return self._get_property('fixedWidthFont')

    @fixed_width_font.setter
    def fixed_width_font(self, value: str):
        self._set_property('fixedWidthFont', value)

    @property
    def fixed_width_font_size(self) -> float:
        return self._get_property('fixedWidthFontSize')

    @fixed_width_font_size.setter
    def fixed_width_font_size(self, value: float):
        self._set_property('fixedWidthFontSize', value)

    @property
    def inbox(self) -> Mailbox:
        """The top level In mailbox."""
        return self._get_property('inbox')

    @property
    def include_all_original_message_text(self) -> bool:
        return self._get_property('includeAllOriginalMessageText')

    @include_all_original_message_text.setter
    def include_all_original_message_text(self, value: bool):
        self._set_property('includeAllOriginalMessageText', value)

    @property
    def quote_original_message(self) -> bool:
        return self._get_property('quoteOriginalMessage')

    @quote_original_message.setter
    def quote_original_message(self, value: bool):
        self._set_property('quoteOriginalMessage', value)

    @property
    def check_spelling_while_typing(self) -> bool:
        return self._get_property('checkSpellingWhileTyping')

    @check_spelling_while_typing.setter
    def check_spelling_while_typing(self, value: bool):
        self._set_property('checkSpellingWhileTyping', value)

    @property
    def junk_mailbox(self) -> Mailbox:
        """The top level Junk mailbox."""
        return self._get_property('junkMailbox')

    @property
    def level_one_quoting_color(self) -> str:
        return self._get_property('levelOneQuotingColor')

    @level_one_quoting_color.setter
    def level_one_quoting_color(self, value: str):
        self._set_property('levelOneQuotingColor', value)

    @property
    def level_two_quoting_color(self) -> str:
        return self._get_property('levelTwoQuotingColor')

    @level_two_quoting_color.setter
    def level_two_quoting_color(self, value: str):
        self._set_property('levelTwoQuotingColor', value)

    @property
    def level_three_quoting_color(self) -> str:
        return self._get_property('levelThreeQuotingColor')

    @level_three_quoting_color.setter
    def level_three_quoting_color(self, value: str):
        self._set_property('levelThreeQuotingColor', value)

    @property
    def message_font(self) -> str:
        return self._get_property('messageFont')

    @message_font.setter
    def message_font(self, value: str):
        self._set_property('messageFont', value)

    @property
    def message_font_size(self) -> float:
        return self._get_property('messageFontSize')

    @message_font_size.setter
    def message_font_size(self, value: float):
        self._set_property('messageFontSize', value)

    @property
    def message_list_font(self) -> str:
        return self._get_property('messageListFont')

    @message_list_font.setter
    def message_list_font(self, value: str):
        self._set_property('messageListFont', value)

    @property
    def message_list_font_size(self) -> float:
        return self._get_property('messageListFontSize')

    @message_list_font_size.setter
    def message_list_font_size(self, value: float):
        self._set_property('messageListFontSize', value)

    @property
    def new_mail_sound(self) -> str:
        return self._get_property('newMailSound')

    @new_mail_sound.setter
    def new_mail_sound(self, value: str):
        self._set_property('newMailSound', value)

    @property
    def outbox(self) -> Mailbox:
        """The top level Out mailbox."""
        return self._get_property('outbox')

    @property
    def should_play_other_mail_sounds(self) -> bool:
        return self._get_property('shouldPlayOtherMailSounds')

    @should_play_other_mail_sounds.setter
    def should_play_other_mail_sounds(self, value: bool):
        self._set_property('shouldPlayOtherMailSounds', value)

    @property
    def same_reply_format(self) -> bool:
        return self._get_property('sameReplyFormat')

    @same_reply_format.setter
    def same_reply_format(self, value: bool):
        self._set_property('sameReplyFormat', value)

    @property
    def selected_signature(self) -> str:
        return self._get_property('selectedSignature')

    @selected_signature.setter
    def selected_signature(self, value: str):
        self._set_property('selectedSignature', value)

    @property
    def sent_mailbox(self) -> Mailbox:
        """The top level Sent mailbox."""
        return self._get_property('sentMailbox')

    @property
    def fetches_automatically(self) -> bool:
        return self._get_property('fetchesAutomatically')

    @fetches_automatically.setter
    def fetches_automatically(self, value: bool):
        self._set_property('fetchesAutomatically', value)

    @property
    def highlight_selected_conversation(self) -> bool:
        return self._get_property('highlightSelectedConversation')

    @highlight_selected_conversation.setter
    def highlight_selected_conversation(self, value: bool):
        self._set_property('highlightSelectedConversation', value)

    @property
    def trash_mailbox(self) -> Mailbox:
        """The top level Trash mailbox."""
        return self._get_property('trashMailbox')

    @property
    def use_address_completion(self) -> bool:
        return self._get_property('useAddressCompletion')

    @property
    def use_fixed_width_font(self) -> bool:
        return self._get_property('useFixedWidthFont')

    @use_fixed_width_font.setter
    def use_fixed_width_font(self, value: bool):
        self._set_property('useFixedWidthFont', value)

    @property
    def primary_email(self) -> str:
        """The user's primary email address."""
        return self._get_property('primaryEmail')
