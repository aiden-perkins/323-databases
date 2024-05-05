from __future__ import annotations
from typing import Iterator

from mongoengine import EnumField

import collection_documents
from utils import print_exception, select_general_embedded, Satisfactory, prompt_for_enum, EmbeddedCollectionInterface


class LetterGrade(EmbeddedCollectionInterface):
    minSatisfactory = EnumField(Satisfactory, db_field='min_satisfactory', required=True)

    parent = 'Enrollment'

    def __str__(self):
        return f'{self.get_document()} wants at least a {self.minSatisfactory.name} in {self.get_parent().section}'

    def get_parent(self) -> collection_documents.Enrollment:
        return self._instance

    def get_document(self) -> collection_documents.Student:
        parent = self._instance
        while isinstance(parent, EmbeddedCollectionInterface):
            parent = parent.get_parent()
        return parent

    @staticmethod
    def add_document(from_enrollment: bool = False) -> LetterGrade:
        while True:
            enrollment = None
            if not from_enrollment:
                print('Select an enrollment: ')
                enrollment = collection_documents.Enrollment.select_document()
                print('Switching from LetterGrade to PassFail:')
            min_satisfactory = prompt_for_enum('Select the minimum satisfactory grade: ', Satisfactory)
            new_letter_grade = LetterGrade(minSatisfactory=min_satisfactory)
            try:
                if not from_enrollment:
                    enrollment.switch_grade_option(letter_grade=new_letter_grade)
                    enrollment.get_document().save()
                return new_letter_grade
            except Exception as e:
                print('Errors storing the new letter grade:')
                print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        letter_grade = LetterGrade.select_document()
        print('Switching from LetterGrade to PassFail:')
        new_pass_fail = collection_documents.PassFail.add_document(from_enrollment=True)
        letter_grade.get_parent().switch_grade_option(pass_fail=new_pass_fail)

    @staticmethod
    def list_documents() -> None:
        for letterGrade in LetterGrade.get_all_objects():
            print(letterGrade)

    @staticmethod
    def select_document() -> LetterGrade:
        enrollment = None
        while not enrollment:
            enrollment = select_general_embedded(collection_documents.Enrollment)
            if enrollment.letterGrade:
                break
            print('That enrollment did not choose letter grade, try again.')
            enrollment = None
        return enrollment.letterGrade

    @staticmethod
    def get_all_objects() -> Iterator[LetterGrade]:
        for student in collection_documents.Student.objects().order_by('first_name', 'last_name'):
            for enrollment in student.enrollments:
                if enrollment.letterGrade:
                    yield enrollment.letterGrade
