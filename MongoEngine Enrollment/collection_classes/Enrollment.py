from __future__ import annotations
from typing import Iterator

from mongoengine import EmbeddedDocument, EmbeddedDocumentField, ReferenceField

import collection_classes
from utils import print_exception, select_general_embedded, unique_general_embedded


class Enrollment(EmbeddedDocument):
    section = ReferenceField('Section', required=True)
    passFail = EmbeddedDocumentField('PassFail', db_field='pass_fail')
    letterGrade = EmbeddedDocumentField('LetterGrade', db_field='letter_grade')

    parent = 'Student'

    # This doesn't actually do anything, this is only here, so I can access it with other functions.
    meta = {
        'indexes': [
            {'unique': True, 'fields': ['parent', 'section'], 'name': 'enrollments_uk_01'},
            {
                'unique': True,
                'fields': ['section.semester', 'section.year', 'section.course', 'parent'],
                'name': 'enrollments_uk_02'
            }
        ]
    }

    def __str__(self):
        return f'{self._instance} is enrolled in {self.section}'

    @staticmethod
    def add_document() -> None:
        success: bool = False
        while not success:
            print('Select a student: ')
            student = collection_classes.Student.select_document()
            print('Select a section: ')
            section = collection_classes.Section.select_document()
            pass_fail = None
            letter_grade = None
            choice = int(input('Do you want pass fail (1) or letter grade (2) --> '))
            if choice == 1:
                pass_fail = collection_classes.PassFail.add_document(from_enrollment=True)
            else:
                letter_grade = collection_classes.LetterGrade.add_document(from_enrollment=True)
            new_enrollment = Enrollment(section=section, passFail=pass_fail, letterGrade=letter_grade)
            new_enrollment._instance = student
            violated_constraints = unique_general_embedded(new_enrollment)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    student.add_enrollment(new_enrollment)
                    student.save()
                    section.add_student(student)
                    section.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new enrollment:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        enrollment = Enrollment.select_document()
        enrollment.section.remove_student(enrollment._instance)
        enrollment.section.save()
        enrollment._instance.remove_enrollment(enrollment)
        enrollment._instance.save()

    @staticmethod
    def list_documents() -> None:
        for enrollment in Enrollment.get_all_objects():
            print(enrollment)

    @staticmethod
    def select_document() -> Enrollment:
        return select_general_embedded(Enrollment)

    @staticmethod
    def get_all_objects() -> Iterator[Enrollment]:
        for student in collection_classes.Student.objects:
            for enrollment in student.enrollments:
                yield enrollment

    def switch_grade_option(
            self, pass_fail: collection_classes.PassFail = None, letter_grade: collection_classes.LetterGrade = None
    ) -> None:
        self.passFail = pass_fail
        self.letterGrade = letter_grade
        self._instance.save()
