from __future__ import annotations

from mongoengine import *

from utils import Semester, Building, Schedule, CollectionInterface
from collection_classes import Course, Student


class Section(Document, CollectionInterface):
    course = ReferenceField(Course, required=True, reverse_delete_rule=DENY)
    sectionNumber = IntField(db_field='section_number', required=True)
    semester = EnumField(Semester, required=True)
    sectionYear = IntField(db_field='section_year', required=True)
    building = EnumField(Building, required=True)
    room = IntField(db_field='room', min_value=1, max_value=999, required=True)
    schedule = EnumField(Schedule, required=True)
    startTime = IntField(db_field='start_time', min_value=800, max_value=1930, required=True)
    instructor = StringField(db_field='instructor', required=True)

    students = ListField(ReferenceField(Student))

    meta = {
        'collection': 'sections',
        'indexes': [
            {'unique': True, 'fields': ['course', 'sectionNumber', 'semester', 'sectionYear'],
             'name': 'sections_uk_01'},
            {'unique': True, 'fields': ['semester', 'sectionYear', 'building', 'room', 'schedule', 'startTime'],
             'name': 'sections_uk_02'},
            {'unique': True, 'fields': ['semester', 'sectionYear', 'schedule', 'startTime', 'instructor'],
             'name': 'sections_uk_03'}
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
    def select_document() -> Section:
        # TODO: finish this method
        pass
