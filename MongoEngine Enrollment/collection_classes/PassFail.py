from __future__ import annotations
import datetime

from mongoengine import EmbeddedDocument, DateTimeField

import collection_classes
from utils import prompt_for_date, print_exception, select_general_embedded


class PassFail(EmbeddedDocument):
    applicationDate = DateTimeField(db_field='application_date', required=True)

    parent = 'Enrollment'

    def __str__(self):
        return f'{self._instance._instance} applied for pass fail on {self.applicationDate} in {self._instance.section}'

    @staticmethod
    def add_document(from_enrollment: bool = False) -> PassFail:
        """
        Create a new PassFail instance.
        :return: None
        """
        while True:
            enrollment = None
            if not from_enrollment:
                print('Select an enrollment: ')
                enrollment = collection_classes.Enrollment.select_document()
            application_date = prompt_for_date('Date and time of the application: ')
            now = datetime.datetime.now()
            if application_date > now:
                print(f'Application date must be before the current time ({now.strftime("%m-%d-%Y %H-%M-%S")})')
                continue
            new_pass_fail = PassFail(applicationDate=application_date)
            try:
                if not from_enrollment:
                    enrollment.switch_grade_option(pass_fail=new_pass_fail)
                    enrollment._instance.save()
                return new_pass_fail
            except Exception as e:
                print('Errors storing the new student major:')
                print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        """
        Delete an existing PassFail from the database.
        :return: None
        """
        pass_fail = PassFail.select_document()
        new_letter_grade = collection_classes.LetterGrade.add_document(from_enrollment=True)
        pass_fail._instance.switch_grade_option(letter_grade=new_letter_grade)

    @staticmethod
    def list_documents() -> None:
        for student in collection_classes.Student.objects:
            for enrollment in student.enrollments:
                if enrollment.passFail:
                    print(enrollment.passFail)

    @staticmethod
    def select_document() -> PassFail:
        enrollment = None
        while not enrollment:
            enrollment = select_general_embedded(collection_classes.Enrollment)
            if enrollment.passFail:
                break
            print('That enrollment did not choose pass fail, try again.')
            enrollment = None
        return enrollment.passFail
