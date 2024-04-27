from __future__ import annotations

from mongoengine import EmbeddedDocument, EmbeddedDocumentField, ReferenceField

from utils import unique_general, print_exception, select_general
from collection_classes import Section, PassFail, LetterGrade, Student


class Enrollment(EmbeddedDocument):
    section = ReferenceField('Section', required=True)
    passFail = EmbeddedDocumentField('PassFail', db_field='pass_fail')
    letterGrade = EmbeddedDocumentField('LetterGrade', db_field='letter_grade')

    meta = {
        'indexes': [
            {'unique': True, 'fields': ['student', 'section'], 'name': 'enrollments_uk_01'},
            {
                'unique': True,
                'fields': ['section.semester', 'section.year', 'section.course', 'student'],
                'name': 'enrollments_uk_02'
            }
        ]
    }

    def __init__(self, section: Section, passFail: PassFail, letterGrade: LetterGrade, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.section = section
        self.passFail = passFail
        self.letterGrade = letterGrade

    def __str__(self):
        return f'{self._instance} is enrolled in {self.section}'

    @staticmethod
    def add_document() -> None:
        success: bool = False
        while not success:
            print('Select a student: ')
            student = Student.select_document()
            print('Select a section: ')
            section = Section.select_document()
            pass_fail = None
            letter_grade = None
            choice = int(input('Do you want pass fail (1) or letter grade (2)?'))
            if choice == 1:
                pass_fail = PassFail.add_document(from_enrollment=True)
            else:
                letter_grade = LetterGrade.add_document(from_enrollment=True)
            new_enrollment = Enrollment(section, pass_fail, letter_grade)
            violated_constraints = unique_general(new_enrollment)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    student.add_enrollment(new_enrollment)
                    student.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new enrollment:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        enrollment = Enrollment.select_document()
        enrollment._instance.remove_enrollment(enrollment)

    @staticmethod
    def list_documents() -> None:
        for student in Student.objects:
            for enrollment in student.enrollments:
                print(enrollment)

    @staticmethod
    def select_document() -> Enrollment:
        return select_general(Enrollment)

    def switch_grade_option(self, pass_fail: PassFail = None, letter_grade: LetterGrade = None):
        self.passFail = pass_fail
        self.letterGrade = letter_grade
