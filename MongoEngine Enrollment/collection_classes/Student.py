from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface
from collection_classes import Enrollment, StudentMajor


class Student(Document, CollectionInterface):
    lastName = StringField(db_field='last_name', required=True)
    firstName = StringField(db_field='first_name', required=True)
    email = StringField(db_field='email', required=True)

    enrollments = EmbeddedDocumentListField(Enrollment, db_field='enrollment')
    studentMajors = EmbeddedDocumentListField(StudentMajor, db_field='student_majors')

    meta = {
        'collection': 'students',
        'indexes': [
            {'unique': True, 'fields': ['lastName', 'firstName'], 'name': 'students_uk_01'},
            {'unique': True, 'fields': ['email'], 'name': 'students_uk_02'},
            {'unique': True, 'fields': ['_id'], 'name': 'students_uk_03'}
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
    def select_document() -> Student:
        # TODO: finish this method
        pass
