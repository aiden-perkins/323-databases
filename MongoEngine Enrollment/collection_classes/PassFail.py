from __future__ import annotations
import datetime

from mongoengine import EmbeddedDocument, DateField

from utils import prompt_for_date, unique_general, print_exception, select_general
from collection_classes import Enrollment, Student


class PassFail(EmbeddedDocument):
    applicationDate = DateField(db_field='application_date', required=True)

    def __init__(self, applicationDate: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applicationDate = applicationDate

    def __str__(self):
        return f'{self._instance._instance} applied on {self.applicationDate} in {self._instance.section}'

    @staticmethod
    def add_document() -> None:
        """
        Create a new PassFail instance.
        :return: None
        """
        success: bool = False
        while not success:
            enrollment = Enrollment.select_document()
            application_date = prompt_for_date('Date and time of the application: ')
            new_pass_fail = PassFail(application_date)
            violated_constraints = unique_general(new_pass_fail)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    enrollment.set_pass_fail(new_pass_fail)
                    enrollment._instance.save()
                    success = True
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
        pass_fail._instance.remove_pass_fail(pass_fail)

    @staticmethod
    def list_documents() -> None:
        for student in Student.objects:
            for enrollment in student.enrollments:
                if enrollment.passFail:
                    print(enrollment.passFail)

    @staticmethod
    def select_document() -> PassFail:
        return select_general(PassFail)
