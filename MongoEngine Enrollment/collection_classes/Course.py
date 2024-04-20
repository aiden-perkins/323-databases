from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface


class Course(Document, CollectionInterface):
    # TODO: add fields

    # TODO: add all the uniqueness constraints
    meta = {
        'collection': 'courses',
        'indexes': [
            {'unique': True, 'fields': [''], 'name': 'courses_uk_01'},
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
    def select_document() -> Course:
        # TODO: finish this method
        pass
