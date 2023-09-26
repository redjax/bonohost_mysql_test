from dataclasses import dataclass, field
from typing import Union
from contextlib import contextmanager

from constants import SSH_HOST, SSH_KEYFILE, SSH_PASSWORD, SSH_PORT, SSH_USER
from constants import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_TYPE, DB_USER

from loguru import logger as log

import sshtunnel


@dataclass
class SSHClient:
    host: str = field(default="")
    port: int = field(default=22)
    user: str = field(default="")
    password: str = field(default="", repr=False)
    keyfile_path: str = field(default="", repr=False)

    def __repr__(self):
        return f"SSHClient(host={self.host!r}, port={self.port!r}, user={self.user!r})"

    @property
    def server(self) -> sshtunnel.SSHTunnelForwarder:
        try:
            _srv: sshtunnel.SSHTunnelForwarder = sshtunnel.SSHTunnelForwarder(
                self.host,
                ssh_username=self.user,
                ssh_private_key=str(self.keyfile_path),
                remote_bind_address=("127.0.0.1", self.port),
            )

            return _srv

        except Exception as exc:
            raise Exception(
                f"Unhandled exception creating SSHTunnelForwarder server. Details: {exc}"
            )


@dataclass
class DBServer:
    host: str = field(default=None)
    port: int = field(default=3306)
    user: str = field(default=None)
    password: str = field(default=None)
    database: str = field(default=None, repr=False)

    ssh_client: SSHClient = field(default=None)
    local_bind_port: int | None = field(default=None)

    def __repr__(self):
        return f"DBServer(host={self.host!r}, port={self.port!r}, user={self.user!r}, database={self.database!r})"
