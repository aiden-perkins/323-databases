from __future__ import annotations
import datetime

from mongoengine import EmbeddedDocument, DateField

from utils import prompt_for_date, unique_general, print_exception, select_general
from collection_classes import Enrollment, Student, LetterGrade


class PassFail(EmbeddedDocument):
    applicationDate = DateField(db_field='application_date', required=True)

    def __init__(self, applicationDate: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applicationDate = applicationDate

    def __str__(self):
        return f'{self._instance._instance} applied on {self.applicationDate} in {self._instance.section}'

    @staticmethod
    def add_document(from_enrollment: bool = False) -> PassFail:
        """
        Create a new PassFail instance.
        :return: None
        """
        while True:
            enrollment = None
            if not from_enrollment:
                enrollment = Enrollment.select_document()
            application_date = prompt_for_date('Date and time of the application: ')
            now = datetime.datetime.now()
            if application_date <= now:
                print(f'Application date must be before the current time ({now.strftime("%m-%d-%Y %H-%M-%S")})')
                continue
            new_pass_fail = PassFail(application_date)
            violated_constraints = unique_general(new_pass_fail)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
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
        new_letter_grade = LetterGrade.add_document(from_enrollment=True)
        pass_fail._instance.switch_grade_option(letter_grade=new_letter_grade)

    @staticmethod
    def list_documents() -> None:
        for student in Student.objects:
            for enrollment in student.enrollments:
                if enrollment.passFail:
                    print(enrollment.passFail)

    @staticmethod
    def select_document() -> PassFail:
        return select_general(PassFail)
