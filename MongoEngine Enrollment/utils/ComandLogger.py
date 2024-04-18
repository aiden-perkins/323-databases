from __future__ import annotations
import logging

from pymongo import monitoring

from utils import logging_menu


class CommandLogger(monitoring.CommandListener):
    _instance: CommandLogger = None
    _initialized: bool = False

    def __new__(cls) -> CommandLogger:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not CommandLogger._initialized:
            super().__init__(*args, **kwargs)
            self.log = logging.getLogger('MongoDB logger')
            log_level = logging_menu.menu_prompt()
            self.log.setLevel(log_level)
            logging.basicConfig(level=log_level)

    def started(self, event):
        self.log.debug(
            f'Command {event.command_name} with request id {event.request_id} started on server {event.connection_id}'
        )

    def succeeded(self, event):
        self.log.debug(
            f'Command {event.command_name} with request id {event.request_id} on server {event.connection_id} '
            f'succeeded in {event.duration_micros} microseconds'
        )

    def failed(self, event):
        self.log.debug(
            f'Command {event.command_name} with request id {event.request_id} on server {event.connection_id} '
            f'failed in {event.duration_micros} microseconds'
        )
