from __future__ import annotations

from mongoengine import Document, StringField, IntField, EnumField, ListField, ReferenceField

import collection_classes
from utils import Building, prompt_for_enum, unique_general, print_exception, select_general


class Department(Document):
    name = StringField(required=True)
    abbreviation = StringField(required=True, max_length=6)
    chairName = StringField(db_field='chair_name', required=True, max_length=80)
    building = EnumField(Building, required=True)
    office = IntField(required=True)
    description = StringField(required=True, max_length=80)

    courses = ListField(ReferenceField('Course'))
    majors = ListField(ReferenceField('Major'))

    meta = {
        'collection': 'departments',
        'indexes': [
            {'unique': True, 'fields': ['name'], 'name': 'departments_uk_01'},
            {'unique': True, 'fields': ['abbreviation'], 'name': 'departments_uk_02'},
            {'unique': True, 'fields': ['chairName'], 'name': 'departments_uk_03'},
            {'unique': True, 'fields': ['building', 'office'], 'name': 'departments_uk_04'},
        ]
    }

    def __str__(self) -> str:
        return self.abbreviation

    @staticmethod
    def add_document() -> None:
        """
        Create a new Department instance.
        :return: None
        """
        success: bool = False
        while not success:
            name = input('Department name --> ')
            abbreviation = input('Department abbreviation --> ')
            chair_name = input('Department chair name --> ')
            building = prompt_for_enum('Department building: ', Building)
            office = int(input('Department office --> '))
            description = input('Department description --> ')

            new_department = Department(
                name=name, abbreviation=abbreviation, chairName=chair_name,
                building=building, office=office, description=description
            )
            violated_constraints = unique_general(new_department)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                # TODO: also add a major to the department so a department always has a major.
                try:
                    new_department.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new department:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        """
        Delete an existing department from the database.
        :return: None
        """
        department = Department.select_document()
        if department.majors:
            print('This department has majors attached to it, delete those first and then try again.')
            return
        if department.courses:
            print('This department has courses attached to it, delete those first and then try again.')
            return
        department.delete()

    @staticmethod
    def list_documents() -> None:
        for department in Department.objects:
            print(department)

    @staticmethod
    def select_document() -> Department:
        return select_general(Department)

    def add_major(self, new_major: collection_classes.Major) -> None:
        for major in self.majors:
            if new_major.pk == major.pk:
                return
        self.majors.append(new_major)

    def remove_major(self, old_major: collection_classes.Major) -> None:
        for major in self.majors:
            if major.pk == old_major.pk:
                self.majors.remove(old_major)
                return

    def add_course(self, new_course: collection_classes.Course) -> None:
        for course in self.courses:
            if new_course.pk == course.pk:
                return
        self.courses.append(new_course)

    def remove_course(self, old_course: collection_classes.Course) -> None:
        for course in self.courses:
            if course.pk == old_course.pk:
                self.courses.remove(old_course)
                return
