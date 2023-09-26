import sys

sys.path.append(".")

import stackprinter

from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, NullPool

from pathlib import Path
from typing import Union
import time
import logging
import shutil

from loguru import logger as log

import pandas as pd

from dynaconf import settings

from red_utils.ext.loguru_utils import init_logger, sinks

from sqlalchemy import create_engine

from red_utils.ext.sqlalchemy_utils import get_session

from constants import (
    ENV,
    DB_DATABASE,
    DB_HOST,
    DB_PASSWORD,
    DB_PORT,
    DB_TYPE,
    DB_USER,
    SSH_HOST,
    SSH_KEYFILE,
    SSH_PASSWORD,
    SSH_USER,
    SSH_PORT,
)

import pymysql
import sshtunnel
from sshtunnel import SSHTunnelForwarder

from domain.mysql_ssh_tun import SSHClient, DBServer

from red_utils.ext.sqlalchemy_utils import (
    get_engine,
    Base,
    get_session,
    create_base_metadata,
)


if __name__ == "__main__":
    stackprinter.set_excepthook(style="darkbg2")

    init_logger(sinks=[sinks.default_stdout_color_sink])

    log.info("App start")

    log.info("Starting SSH connection")

    log.debug(f"Using keyfile: {SSH_KEYFILE}")

    ## Get an SSH client
    ssh_client: SSHClient = SSHClient(
        host=SSH_HOST,
        port=SSH_PORT,
        user=SSH_USER,
        password=SSH_PASSWORD,
        keyfile_path=SSH_KEYFILE,
    )
    log.debug(f"SSH client: {ssh_client}")

    ## Create database server object
    db_server: DBServer = DBServer(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        ssh_client=ssh_client.server,
    )
    log.debug(f"DB Server: {db_server}")

    with db_server.ssh_client as db_ssh:
        db_server.local_bind_port = db_ssh.local_bind_port
        log.debug(f"Local bind port: {db_server.local_bind_port}")
        engine = create_engine(
            f"mysql+pymysql://{db_server.user}:{db_server.password}@localhost:{int(db_server.local_bind_port)}/{db_server.database}",
            ## Fix "pymysql.err.InternalError) Packet sequence number wrong"
            poolclass=NullPool,
        )

        SessionLocal = get_session(engine=engine)

        try:
            with SessionLocal() as sess:
                log.debug(f"Engine connection successful.")

        except Exception as exc:
            raise Exception(
                f"Unhandled exception connecting to MySQL database over SSH tunnel. Details: {exc}"
            )
