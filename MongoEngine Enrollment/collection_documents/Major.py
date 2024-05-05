from __future__ import annotations

from mongoengine import ReferenceField, StringField, DENY

import collection_documents
from utils import unique_general, print_exception, select_general, CollectionInterface


class Major(CollectionInterface):
    department = ReferenceField('Department', required=True, reverse_delete_rule=DENY)
    name = StringField(required=True)
    description = StringField(required=True)

    meta = {
        'collection': 'majors',
        'indexes': [
            {'unique': True, 'fields': ['name'], 'name': 'majors_uk_01'},
        ]
    }

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def add_document() -> None:
        success: bool = False
        while not success:
            print('Select a department: ')
            department = collection_documents.Department.select_document()
            name = input('Major name --> ')
            description = input('Major description --> ')
            new_major = Major(department=department, name=name, description=description)
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
        major = Major.select_document()
        for student in collection_documents.Student.objects:
            for student_major in student.studentMajors:
                if student_major.major.pk == major.pk:
                    print('There is a student with this major, cannot delete this major.')
                    return
        major.department.remove_major(major)
        major.department.save()
        major.delete()

    @staticmethod
    def list_documents() -> None:
        for major in Major.objects().order_by('name'):
            print(major)

    @staticmethod
    def select_document() -> Major:
        return select_general(Major)
