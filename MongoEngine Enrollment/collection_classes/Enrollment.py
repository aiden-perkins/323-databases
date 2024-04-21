from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface
from collection_classes import Section, Student, PassFail, LetterGrade


class Enrollment(EmbeddedDocument, CollectionInterface):
    section = ReferenceField(Section, required=True)
    student = ReferenceField(Student, required=True, reverse_delete_rule=DENY)
    passFail = EmbeddedDocumentField(PassFail, db_field='pass_fail')
    letterGrade = EmbeddedDocumentField(LetterGrade, db_field='letter_grade')

    meta = {
        'collection': 'enrollments',
        'indexes': [
            {'unique': True, 'fields': ['student', 'section'], 'name': 'enrollments_uk_01'},
            {'unique': True, 'fields': ['section.semester', 'section.sectionYear', 'section.course', 'student'],
             'name': 'enrollments_uk_02'}
        ]
    }

    def __init__(self, section: Section, passFail: PassFail, letterGrade: LetterGrade, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.section = section
        self.passFail = passFail
        self.letterGrade = letterGrade

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
    def select_document() -> Enrollment:
        # TODO: finish this method
        pass

