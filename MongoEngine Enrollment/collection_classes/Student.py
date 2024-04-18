from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface
from collection_classes import Enrollment


class Student(Document, CollectionInterface):
    # TODO: add fields
    enrollments = EmbeddedDocumentListField(Enrollment, db_field='enrollment')

    # TODO: add all the uniqueness constraints
    meta = {
        'collection': 'students',
        'indexes': [
            {'unique': True, 'fields': [''], 'name': 'students_uk_01'},
        ]
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # TODO: finish initializing variables

    def __str__(self) -> str:
        # TODO: finish this method
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

    def select_document(self) -> Student:
        # TODO: finish this method
        pass
