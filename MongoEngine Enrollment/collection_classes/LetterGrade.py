from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface


class LetterGrade(EmbeddedDocument, CollectionInterface):
    # TODO: add fields

    # TODO: add all the uniqueness constraints
    meta = {
        'collection': 'letter_grade',
        'indexes': [
            {'unique': True, 'fields': [''], 'name': 'letter_grade_uk_01'},
        ]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: finish initializing variables

    def __str__(self):
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
    def select_document() -> LetterGrade:
        # TODO: finish this method
        pass
