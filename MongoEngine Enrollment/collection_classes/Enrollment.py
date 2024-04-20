from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface
from collection_classes import Section, PassFail, LetterGrade


class Enrollment(EmbeddedDocument, CollectionInterface):
    # TODO: fix the parameters in here because they are wrong
    section = ReferenceField(Section, required=True)
    passFail = EmbeddedDocumentField(PassFail)
    letterGrade = EmbeddedDocumentField(LetterGrade)

    # TODO: add all the uniqueness constraints
    meta = {
        'collection': 'enrollments',
        'indexes': [
            {'unique': True, 'fields': [''], 'name': 'enrollments_uk_01'},
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

