import json
import logging
from typing import List

from ..models.msg import MsgMessage, MsgError

from .msg import _MsgClient

import proton
import proton.utils
from proton.reactor import Container

LOG = logging.getLogger("pubtools.sign.signers.radas")


class _SendClient(_MsgClient):
    def __init__(
        self,
        messages: List[MsgMessage],
        broker_urls: List[str],
        cert: str,
        ca_cert: str,
        errors: List[MsgError],
    ):
        super().__init__(errors=errors)
        self.broker_urls = broker_urls
        self.messages = messages
        self.ssl_domain = proton.SSLDomain(proton.SSLDomain.MODE_CLIENT)
        if cert:
            self.ssl_domain.set_credentials(cert, cert, None)
        if ca_cert:
            self.ssl_domain.set_trusted_ca_db(ca_cert)
        self.ssl_domain.set_peer_authentication(proton.SSLDomain.ANONYMOUS_PEER)
        self.sent = 0
        self.confirmed = 0
        self.total = len(messages)

    def on_start(self, event):
        conn = event.container.connect(
            urls=self.broker_urls, ssl_domain=self.ssl_domain, sasl_enabled=False
        )
        self.sender = event.container.create_sender(conn)

    def on_sendable(self, event):
        LOG.debug("Sender on_sendable")
        if self.sent < self.total:
            message = self.messages[self.sent]
            LOG.debug("Sending message: %s %s %s", message.body, message.address, message.headers)
            event.sender.send(
                proton.Message(
                    properties=message.headers,
                    address=message.address,
                    body=json.dumps(message.body),
                )
            )
            self.sent += 1

    def on_accepted(self, event):
        LOG.debug("Sender accepted")
        self.confirmed += 1
        if self.confirmed == self.total:
            LOG.debug("Sender closing")
            event.connection.close()

    def on_disconnected(self, event):  # pragma: no cover
        self.sent = self.confirmed  # pragma: no cover


class SendClient(Container):
    """SendClient wrapper class."""

    def __init__(
        self,
        messages: List[MsgMessage],
        broker_urls: List[str],
        cert: str,
        ca_cert: str,
        retries: int,
        errors: List[MsgError],
    ):
        """Send Client Initializer.

        :param messages: List of messages to send.
        :type messages: List[MsgMessage]
        :param broker_urls: List of addresses of messaging broker
        :type messages: List[str]
        :param cert: Messaging client certificate
        :type cert: str
        :param retries: Number of retries for sending messages
        :type retries: int
        :param errors: List of errors which occured during the process
        :type errors: List[MsgError]
        """
        self.messages = messages
        self.handler = _SendClient(
            messages=messages, broker_urls=broker_urls, cert=cert, ca_cert=ca_cert, errors=errors
        )
        self._retries = retries
        self._errors = errors
        super().__init__(self.handler)

    def run(self):
        """Run the SendClient."""
        errors_len = 0
        if not len(self.messages):
            LOG.warning("No messages to send")
            return []
        for x in range(self._retries):
            super().run()
            if len(self._errors) == errors_len:
                break
            errors_len = len(self._errors)
        else:
            return self._errors
        return []
