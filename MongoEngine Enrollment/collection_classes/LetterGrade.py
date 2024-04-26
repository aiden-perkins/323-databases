from __future__ import annotations

from mongoengine import EmbeddedDocument, StringField

from utils import print_exception, unique_general, select_general, Satisfactory, prompt_for_enum
from collection_classes import Enrollment, Student


class LetterGrade(EmbeddedDocument):
    minSatisfactory = StringField(db_field='min_satisfactory', required=True)

    def __init__(self, minSatisfactory: Satisfactory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minSatisfactory = minSatisfactory

    def __str__(self):
        return f'{self._instance._instance} wants at least a {self.minSatisfactory} in {self._instance.section}'

    @staticmethod
    def add_document() -> None:
        success: bool = False
        while not success:
            enrollment = Enrollment.select_document()
            min_satisfactory = prompt_for_enum(
                'Select the minimum satisfactory grade: ', Satisfactory, 'min_satisfactory'
            )
            new_letter_grade = LetterGrade(min_satisfactory)
            violated_constraints = unique_general(new_letter_grade)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    enrollment.set_letter_grade(new_letter_grade)
                    enrollment._instance.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new department:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        letter_grade = LetterGrade.select_document()
        letter_grade._instance.remove_letter_grade()

    @staticmethod
    def list_documents() -> None:
        for student in Student.objects:
            for enrollment in student.enrollments:
                if enrollment.letterGrade:
                    print(enrollment.letterGrade)

    @staticmethod
    def select_document() -> LetterGrade:
        return select_general(LetterGrade)
