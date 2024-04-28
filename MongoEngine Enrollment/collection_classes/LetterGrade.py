from __future__ import annotations

from mongoengine import EmbeddedDocument, EnumField

import collection_classes
from utils import print_exception, select_general_embedded, Satisfactory, prompt_for_enum


class LetterGrade(EmbeddedDocument):
    minSatisfactory = EnumField(Satisfactory, db_field='min_satisfactory', required=True)

    parent = 'Enrollment'

    def __str__(self):
        return f'{self._instance._instance} wants at least a {self.minSatisfactory.name} in {self._instance.section}'

    @staticmethod
    def add_document(from_enrollment: bool = False) -> LetterGrade:
        while True:
            enrollment = None
            if not from_enrollment:
                print('Select an enrollment: ')
                enrollment = collection_classes.Enrollment.select_document()
            min_satisfactory = prompt_for_enum('Select the minimum satisfactory grade: ', Satisfactory)
            new_letter_grade = LetterGrade(minSatisfactory=min_satisfactory)
            try:
                if not from_enrollment:
                    enrollment.switch_grade_option(letter_grade=new_letter_grade)
                    enrollment._instance.save()
                return new_letter_grade
            except Exception as e:
                print('Errors storing the new letter grade:')
                print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        letter_grade = LetterGrade.select_document()
        new_pass_fail = collection_classes.PassFail.add_document(from_enrollment=True)
        letter_grade._instance.switch_grade_option(pass_fail=new_pass_fail)

    @staticmethod
    def list_documents() -> None:
        for student in collection_classes.Student.objects:
            for enrollment in student.enrollments:
                if enrollment.letterGrade:
                    print(enrollment.letterGrade)

    @staticmethod
    def select_document() -> LetterGrade:
        enrollment = None
        while not enrollment:
            enrollment = select_general_embedded(collection_classes.Enrollment)
            if enrollment.letterGrade:
                break
            print('That enrollment did not choose letter grade, try again.')
        return enrollment.letterGrade
