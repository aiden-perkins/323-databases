from __future__ import annotations

from mongoengine import Document, ReferenceField, StringField, DENY

from utils import unique_general, print_exception, select_general
from collection_classes import Department, Student


class Major(Document):
    department = ReferenceField('Department', required=True)
    name = StringField(required=True)
    description = StringField(required=True)

    meta = {
        'collection': 'majors',
        'indexes': [
            {'unique': True, 'fields': ['name'], 'name': 'majors_uk_01'},
        ]
    }

    def __init__(self, department: Department, name: str, description: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.department = department
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def add_document() -> None:
        """
        Create a new Major instance.
        :return: None
        """
        success: bool = False
        while not success:
            print('Select a department: ')
            department = Department.select_document()
            name = input('Major name --> ')
            description = input('Major description --> ')
            new_major = Major(department, name, description)
            violated_constraints = unique_general(new_major)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    new_major.save()
                    department.add_major(new_major)
                    department.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new major:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        """
        Delete an existing major from the database.
        :return: None
        """
        major = Major.select_document()
        for student in Student.objects:
            for student_major in student.studentMajors:
                if student_major.major.pk == major.pk:
                    print('There is a student with this major, cannot delete this major.')
                    return
        if len(major.department.majors) == 1:
            print('Cannot remove the only major from this department, add another one before deleting this one.')
            return
        major.department.remove_major(major)
        major.delete()

    @staticmethod
    def list_documents() -> None:
        for major in Major.objects:
            print(major)

    @staticmethod
    def select_document() -> Major:
        return select_general(Major)
