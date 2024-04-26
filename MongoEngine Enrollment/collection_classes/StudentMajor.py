from __future__ import annotations
import datetime

from mongoengine import EmbeddedDocument, ReferenceField, DateField, DENY

from utils import prompt_for_date, unique_general, print_exception, select_general
from collection_classes import Major, Student


class StudentMajor(EmbeddedDocument):
    major = ReferenceField(Major, required=True, reverse_delete_rule=DENY)
    declarationDate = DateField(db_field='declaration_date', required=True)

    meta = {
        'indexes': [
            {'unique': True, 'fields': ['student', 'major'], 'name': 'student_majors_uk_01'},
        ]
    }

    def __init__(self, major: Major, declarationDate: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.major = major
        self.declarationDate = declarationDate

    def __str__(self):
        return f'{self._instance} declared {self.major} on {self.declarationDate}'

    @staticmethod
    def add_document() -> None:
        """
        Create a new StudentMajor instance.
        :return: None
        """
        success: bool = False
        while not success:
            major = Major.select_document()
            student = Student.select_document()
            declaration_date = prompt_for_date('Date and time of the declaration: ')
            new_student_major = StudentMajor(major, declaration_date)
            violated_constraints = unique_general(new_student_major)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    student.add_major(new_student_major)
                    student.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new student major:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        """
        Delete an existing student major from the database.
        :return: None
        """
        student_major = StudentMajor.select_document()
        student_major._instance.remove_student_major(student_major)

    @staticmethod
    def list_documents() -> None:
        for student in Student.objects:
            for student_major in student.studentMajors:
                print(student_major)

    @staticmethod
    def select_document() -> StudentMajor:
        return select_general(StudentMajor)
