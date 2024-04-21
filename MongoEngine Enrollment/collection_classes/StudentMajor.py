from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface
from collection_classes import Major, Student


class StudentMajor(EmbeddedDocument, CollectionInterface):
    student = ReferenceField(Student, required=True, reverse_delete_rule=DENY)
    major = ReferenceField(Major, required=True, reverse_delete_rule=DENY)
    declarationDate = DateField(db_field='declaration_date', required=True)

    meta = {
        'collection': 'student_majors',
        'indexes': [
            {'unique': True, 'fields': ['student', 'major'], 'name': 'student_majors_uk_01'},
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
    def select_document() -> StudentMajor:
        # TODO: finish this method
        pass
