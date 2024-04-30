from __future__ import annotations
import datetime
from typing import Iterator

from mongoengine import EmbeddedDocument, ReferenceField, DateTimeField

import collection_classes
from utils import prompt_for_date, print_exception, select_general_embedded, unique_general_embedded


class StudentMajor(EmbeddedDocument):
    major = ReferenceField('Major', required=True)
    declarationDate = DateTimeField(db_field='declaration_date', required=True)

    parent = 'Student'

    # This doesn't actually do anything, this is only here, so I can access it with other functions.
    meta = {
        'indexes': [
            {'unique': True, 'fields': ['parent', 'major'], 'name': 'student_majors_uk_01'},
        ]
    }

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
            print('Select a major: ')
            major = collection_classes.Major.select_document()
            print('Select a student: ')
            student = collection_classes.Student.select_document()
            declaration_date = prompt_for_date('Date and time of the declaration: ')
            now = datetime.datetime.now()
            if declaration_date > now:
                print(f'Declaration date must be before the current time ({now.strftime("%m-%d-%Y %H-%M-%S")})')
                continue
            new_student_major = StudentMajor(major=major, declarationDate=declaration_date)
            new_student_major._instance = student
            violated_constraints = unique_general_embedded(new_student_major)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    student.add_student_major(new_student_major)
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
        student_major._instance.save()

    @staticmethod
    def list_documents() -> None:
        for student_major in StudentMajor.get_all_objects():
            print(student_major)

    @staticmethod
    def select_document() -> StudentMajor:
        return select_general_embedded(StudentMajor)

    @staticmethod
    def get_all_objects() -> Iterator[StudentMajor]:
        for student in collection_classes.Student.objects:
            for student_major in student.studentMajors:
                yield student_major
