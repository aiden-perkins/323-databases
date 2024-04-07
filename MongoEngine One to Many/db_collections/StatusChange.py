import datetime

from mongoengine import *

from db_collections import Status


class StatusChange(EmbeddedDocument):
    """
    Each time the status changes for an order, another instance of this class is
    added to the list of status changes for that order.  They will always be
    appended to the end of the list, and never deleted, so that makes it pretty
    easy to manage the list of status changes.
    """
    status = EnumField(Status, default=Status.IN_PROCESS, required=True)
    statusChangeDate = DateTimeField(db_field='status_change_date', required=True)

    def __init__(self, status: Status, status_change_date: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = status
        self.statusChangeDate = status_change_date

    def __str__(self):
        return f'Status Change Entry: New status: {self.status}, on date: {self.statusChangeDate}'
