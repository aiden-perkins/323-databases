from __future__ import annotations

from mongoengine import StringField, EmbeddedDocumentListField, Document

import collection_classes
from utils import unique_general, print_exception, select_general, unique_general_embedded


class Student(Document):
    lastName = StringField(db_field='last_name', required=True)
    firstName = StringField(db_field='first_name', required=True)
    email = StringField(required=True)

    enrollments = EmbeddedDocumentListField('Enrollment')
    studentMajors = EmbeddedDocumentListField('StudentMajor', db_field='student_majors')

    meta = {
        'collection': 'students',
        'indexes': [
            {'unique': True, 'fields': ['lastName', 'firstName'], 'name': 'students_uk_01'},
            {'unique': True, 'fields': ['email'], 'name': 'students_uk_02'}
        ]
    }

    def __str__(self) -> str:
        return f'{self.firstName} {self.lastName}'

    @staticmethod
    def add_document() -> None:
        """
        Create a new Student instance.
        :return: None
        """
        success: bool = False
        while not success:
            last_name = input('Student last name --> ')
            first_name = input('Student first name --> ')
            email = input('Student email --> ')
            new_student = Student(lastName=last_name, firstName=first_name, email=email)
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
            return
        if student.studentMajors:
            print('This student has majors attached to it, delete those first and then try again.')
            return
        student.delete()

    @staticmethod
    def list_documents() -> None:
        for student in Student.objects:
            print(student)

    @staticmethod
    def select_document() -> Student:
        return select_general(Student)

    def add_enrollment(self, new_enrollment: collection_classes.Enrollment) -> None:
        violations = unique_general_embedded(new_enrollment)
        # This check is pointless, but I left it here as a redundancy, as we already know it's unique because
        # Enrollment.add_document() checks before calling this function. This applies to all add_child() functions.
        if len(violations) < 1:
            self.enrollments.append(new_enrollment)

    def remove_enrollment(self, old_enrollment: collection_classes.Enrollment) -> None:
        violations = unique_general_embedded(old_enrollment)
        # This check is pointless, but I left it here as a redundancy, as we already know it's in enrollments because
        # this function is called from the parent object of the enrollment. This applies to all remove_child functions.
        if len(violations) >= 1:
            self.enrollments.remove(old_enrollment)

    def add_student_major(self, new_student_major: collection_classes.StudentMajor) -> None:
        violations = unique_general_embedded(new_student_major)
        if len(violations) < 1:
            self.studentMajors.append(new_student_major)

    def remove_student_major(self, old_student_major: collection_classes.StudentMajor) -> None:
        violations = unique_general_embedded(old_student_major)
        if len(violations) >= 1:
            self.studentMajors.remove(old_student_major)
