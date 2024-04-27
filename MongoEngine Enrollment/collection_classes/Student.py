from __future__ import annotations

from mongoengine import StringField, EmbeddedDocumentListField, Document

from utils import unique_general, print_exception, select_general
from collection_classes import Enrollment, StudentMajor


class Student(Document):
    lastName = StringField(db_field='last_name', required=True)
    firstName = StringField(db_field='first_name', required=True)
    email = StringField(required=True)

    enrollments = EmbeddedDocumentListField(Enrollment, db_field='enrollment')
    studentMajors = EmbeddedDocumentListField(StudentMajor, db_field='student_majors')

    meta = {
        'collection': 'students',
        'indexes': [
            {'unique': True, 'fields': ['lastName', 'firstName'], 'name': 'students_uk_01'},
            {'unique': True, 'fields': ['email'], 'name': 'students_uk_02'}
        ]
    }

    def __init__(self, lastName: str, firstName: str, email: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.enrollments:
            self.enrollments = []
        if not self.studentMajors:
            self.studentMajors = []
        self.lastName = lastName
        self.firstName = firstName
        self.email = email

    def __str__(self) -> str:
        return f'{self.lastName}, {self.firstName}: {self.email}'

    @staticmethod
    def add_document() -> None:
        """
        Create a new Student instance.
        :return: None
        """
        success: bool = False
        while not success:
            last_name = input('Student last name -->')
            first_name = input('Student first name -->')
            email = input('Student email -->')
            new_student = Student(last_name, first_name, email)
            violated_constraints = unique_general(new_student)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    new_student.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new student:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        """
        Delete an existing student from the database.
        :return: None
        """
        student = Student.select_document()
        if student.enrollments:
            print('This student has enrollments attached to it, delete those first and then try again.')
        if student.studentMajors:
            print("This student has majors attached to it, delete those first and then try again.")
        student.delete()

    @staticmethod
    def list_documents() -> None:
        for student in Student.objects:
            print(student)

    @staticmethod
    def select_document() -> Student:
        return select_general(Student)

    def add_enrollment(self, new_enrollment: Enrollment) -> None:
        for enrollment in self.enrollments:
            # TODO: Enrollment objects do not have an _id, as they are embedded.
            if new_enrollment.pk == enrollment.pk:
                return
        self.enrollments.append(new_enrollment)

    def remove_enrollment(self, old_enrollment: Enrollment) -> None:
        for enrollment in self.enrollments:
            # TODO: Enrollment objects do not have an _id, as they are embedded.
            if enrollment.pk == old_enrollment.pk:
                self.enrollments.remove(old_enrollment)
                return

    def add_student_major(self, new_student_major) -> None:
        for student_major in self.studentMajors:
            if new_student_major.pk == student_major.pk:
                return
        self.studentMajors.append(new_student_major)

    def remove_student_major(self, old_student_major) -> None:
        for student_major in self.studentMajors:
            if student_major.pk == old_student_major.pk:
                self.studentMajors.remove(old_student_major)
                return
