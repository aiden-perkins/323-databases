from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface
from collection_classes import Department


class Major(Document, CollectionInterface):
    department = ReferenceField(Department, required=True, reverse_delete_rule=DENY)
    name = StringField(db_field='name', required=True)
    description = StringField(db_field='description', required=True)

    meta = {
        'collection': 'majors',
        'indexes': [
            {'unique': True, 'fields': ['name'], 'name': 'majors_uk_01'},
        ]
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # TODO: finish initializing variables

    def __str__(self) -> str:
        # TODO: finish this method
        return ''

    @staticmethod
    def add_document() -> None:
        # TODO: finish this method
        pass

    @staticmethod
    def delete_document() -> None:
        # TODO: finish this method
        pass

    @staticmethod
    def list_documents() -> None:
        # TODO: finish this method
        pass

    @staticmethod
    def select_document() -> Major:
        # TODO: finish this method
        pass
