from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface
from collection_classes import Department, Section


class Course(Document, CollectionInterface):
    department = ReferenceField(Department, required=True, reverse_delete_rule=DENY)
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=699, required=True)
    courseName = StringField(db_field='course_name', required=True)
    description = StringField(db_field='description', required=True)
    units = IntField(db_field='units', min_value=1, max_value=5, required=True)

    sections = ListField(ReferenceField(Section))

    meta = {
        'collection': 'courses',
        'indexes': [
            {'unique': True, 'fields': ['department', 'courseNumber'], 'name': 'courses_uk_01'},
            {'unique': True, 'fields': ['department', 'courseName'], 'name': 'courses_uk_02'}
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
