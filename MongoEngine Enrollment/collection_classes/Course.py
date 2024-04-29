from __future__ import annotations

from mongoengine import Document, ReferenceField, IntField, StringField, ListField, DENY

import collection_classes
from utils import unique_general, print_exception, select_general


class Course(Document):
    department = ReferenceField('Department', required=True, reverse_delete_rule=DENY)
    number = IntField(min_value=100, max_value=699, required=True)
    name = StringField(required=True)
    description = StringField(required=True)
    units = IntField(min_value=1, max_value=5, required=True)

    sections = ListField(ReferenceField('Section'))

    meta = {
        'collection': 'courses',
        'indexes': [
            {'unique': True, 'fields': ['department', 'number'], 'name': 'courses_uk_01'},
            {'unique': True, 'fields': ['department', 'name'], 'name': 'courses_uk_02'}
        ]
    }

    def __str__(self) -> str:
        return f'{self.department} {self.number} {self.name} ({self.units}u)'

    @staticmethod
    def add_document() -> None:
        """
        Create a new Course instance
        :return: None
        """
        success: bool = False
        while not success:
            print('Select a department this course belongs to: ')
            department = collection_classes.Department.select_document()
            number = int(input('Course number --> '))
            name = input('Course name --> ')
            description = input('Course description --> ')
            units = int(input('Course units --> '))
            new_course = Course(department=department, number=number, name=name, description=description, units=units)
            violated_constraints = unique_general(new_course)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    new_course.save()
                    department.add_course(new_course)
                    department.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new course:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        course = Course.select_document()
        if course.sections:
            print('This course has sections attached to it, delete those first and then try again.')
            return
        course.department.remove_course(course)
        course.delete()

    @staticmethod
    def list_documents() -> None:
        for course in Course.objects:
            print(course)

    @staticmethod
    def select_document() -> Course:
        return select_general(Course)

    def add_section(self, new_section: collection_classes.Section):
        for section in self.sections:
            if new_section.pk == section.pk:
                return
        self.sections.append(new_section)

    def remove_section(self, old_section: collection_classes.Section):
        for section in self.sections:
            if old_section.pk == section.pk:
                self.sections.remove(old_section)
                return
