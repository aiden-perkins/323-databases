from __future__ import annotations
from typing import Iterator

from mongoengine import EmbeddedDocumentField, ReferenceField

import collection_documents
from utils import print_exception, select_general_embedded, unique_general_embedded, EmbeddedCollectionInterface


class Enrollment(EmbeddedCollectionInterface):
    section = ReferenceField('Section', required=True)
    passFail = EmbeddedDocumentField('PassFail', db_field='pass_fail')
    letterGrade = EmbeddedDocumentField('LetterGrade', db_field='letter_grade')

    parent = 'Student'

    # This doesn't actually do anything within mongodb, this is only here, so I can access it with other functions.
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
        return f'{self.get_document()} is enrolled in {self.section}'

    def get_parent(self) -> collection_documents.Student:
        return self._instance

    def get_document(self) -> collection_documents.Student:
        parent = self._instance
        while isinstance(parent, EmbeddedCollectionInterface):
            parent = parent.get_parent()
        return parent

    @staticmethod
    def add_document() -> None:
        success: bool = False
        while not success:
            print('Select a student: ')
            student = collection_documents.Student.select_document()
            print('Select a section: ')
            section = collection_documents.Section.select_document()
            pass_fail = None
            letter_grade = None
            choice = int(input('Do you want pass fail (1) or letter grade (2) --> '))
            if choice == 1:
                pass_fail = collection_documents.PassFail.add_document(from_enrollment=True)
            else:
                letter_grade = collection_documents.LetterGrade.add_document(from_enrollment=True)
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
        enrollment.section.remove_student(enrollment.get_document())
        enrollment.section.save()
        enrollment.get_document().remove_enrollment(enrollment)
        enrollment.get_document().save()

    @staticmethod
    def list_documents() -> None:
        for enrollment in Enrollment.get_all_objects():
            print(enrollment)

    @staticmethod
    def select_document() -> Enrollment:
        return select_general_embedded(Enrollment)

    @staticmethod
    def get_all_objects() -> Iterator[Enrollment]:
        for student in collection_documents.Student.objects().order_by('first_name', 'last_name'):
            for enrollment in student.enrollments:
                yield enrollment

    def switch_grade_option(
            self, pass_fail: collection_documents.PassFail = None, letter_grade: collection_documents.LetterGrade = None
    ) -> None:
        """
        Switch the enrollment's grade option to either a pass fail or letter
        grade. Must only provide one argument to ensure an enrollment will only
        ever consist of one grade option.

        :param pass_fail:       (optional) The new pass fail object for the
                                enrollment.
        :param letter_grade:    (optional) The new letter grade object for the
                                enrollment.
        :return:                None
        """
        if (pass_fail is None and letter_grade is None) or (pass_fail is not None and letter_grade is not None):
            print('You must provide only one argument.')
            return
        self.passFail = pass_fail
        self.letterGrade = letter_grade
        self.get_document().save()
