from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface


class StudentMajor(EmbeddedDocument, CollectionInterface):
    # TODO: add fields

    # TODO: add all the uniqueness constraints
    meta = {
        'collection': 'student_majors',
        'indexes': [
            {'unique': True, 'fields': [''], 'name': 'student_majors_uk_01'},
        ]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: finish initializing variables

    def __str__(self):
        return ''

    def add_document(self) -> None:
        # TODO: finish this method
        pass

    def delete_document(self) -> None:
        # TODO: finish this method
        pass

    def list_documents(self) -> None:
        # TODO: finish this method
        pass

    def select_document(self) -> StudentMajor:
        # TODO: finish this method
        pass
