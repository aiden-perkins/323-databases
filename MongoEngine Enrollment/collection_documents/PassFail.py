from __future__ import annotations
import datetime
from typing import Iterator

from mongoengine import DateTimeField

import collection_documents
from utils import prompt_for_date, print_exception, select_general_embedded, EmbeddedCollectionInterface


class PassFail(EmbeddedCollectionInterface):
    applicationDate = DateTimeField(db_field='application_date', required=True)

    parent = 'Enrollment'

    def __str__(self):
        return f'{self.get_document()} applied for pass fail on {self.applicationDate} in {self.get_parent().section}'

    def get_parent(self) -> collection_documents.Enrollment:
        return self._instance

    def get_document(self) -> collection_documents.Student:
        parent = self._instance
        while isinstance(parent, EmbeddedCollectionInterface):
            parent = parent.get_parent()
        return parent

    @staticmethod
    def add_document(from_enrollment: bool = False) -> PassFail:
        while True:
            enrollment = None
            if not from_enrollment:
                print('Select an enrollment: ')
                enrollment = collection_documents.Enrollment.select_document()
                print('Switching from PassFail to LetterGrade:')
            application_date = prompt_for_date('Date and time of the application: ')
            now = datetime.datetime.now()
            if application_date > now:
                print(f'Application date must be before the current time ({now.strftime("%m-%d-%Y %H-%M-%S")})')
                continue
            new_pass_fail = PassFail(applicationDate=application_date)
            try:
                if not from_enrollment:
                    enrollment.switch_grade_option(pass_fail=new_pass_fail)
                    enrollment.get_document().save()
                return new_pass_fail
            except Exception as e:
                print('Errors storing the new student major:')
                print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        pass_fail = PassFail.select_document()
        print('Switching from PassFail to LetterGrade:')
        new_letter_grade = collection_documents.LetterGrade.add_document(from_enrollment=True)
        pass_fail.get_parent().switch_grade_option(letter_grade=new_letter_grade)

    @staticmethod
    def list_documents() -> None:
        for passFail in PassFail.get_all_objects():
            print(passFail)

    @staticmethod
    def select_document() -> PassFail:
        enrollment = None
        while not enrollment:
            enrollment = select_general_embedded(collection_documents.Enrollment)
            if enrollment.passFail:
                break
            print('That enrollment did not choose pass fail, try again.')
            enrollment = None
        return enrollment.passFail

    @staticmethod
    def get_all_objects() -> Iterator[PassFail]:
        for student in collection_documents.Student.objects().order_by('first_name', 'last_name'):
            for enrollment in student.enrollments:
                if enrollment.passFail:
                    yield enrollment.passFail
