from __future__ import annotations

from mongoengine import EmbeddedDocument, EnumField

from utils import print_exception, unique_general, select_general, Satisfactory, prompt_for_enum
from collection_classes import Enrollment, Student, PassFail


class LetterGrade(EmbeddedDocument):
    minSatisfactory = EnumField(Satisfactory, db_field='min_satisfactory', required=True)

    def __init__(self, minSatisfactory: Satisfactory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minSatisfactory = minSatisfactory

    def __str__(self):
        return f'{self._instance._instance} wants at least a {self.minSatisfactory} in {self._instance.section}'

    @staticmethod
    def add_document(from_enrollment: bool = False) -> LetterGrade:
        while True:
            enrollment = None
            if not from_enrollment:
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
        new_pass_fail = PassFail.add_document(from_enrollment=True)
        letter_grade._instance.switch_grade_option(pass_fail=new_pass_fail)

    @staticmethod
    def list_documents() -> None:
        for student in Student.objects:
            for enrollment in student.enrollments:
                if enrollment.letterGrade:
                    print(enrollment.letterGrade)

    @staticmethod
    def select_document() -> LetterGrade:
        return select_general(LetterGrade)
