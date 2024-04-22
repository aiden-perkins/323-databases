from __future__ import annotations

from mongoengine import *

from utils import CollectionInterface, unique_general, print_exception, select_general
from collection_classes import Department, Section


class Course(Document, CollectionInterface):
    department = ReferenceField(Department, required=True, reverse_delete_rule=DENY)
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=699, required=True)
    courseName = StringField(db_field='course_name', required=True)
    description = StringField(db_field='description', required=True)
    units = IntField(db_field='units', min_value=1, max_value=5, required=True)

    sections = ListField(ReferenceField(Section))

    meta = {
        'collection': 'courses',
        'indexes': [
            {'unique': True, 'fields': ['department', 'courseNumber'], 'name': 'courses_uk_01'},
            {'unique': True, 'fields': ['department', 'courseName'], 'name': 'courses_uk_02'}
        ]
    }

    def __init__(
            self,
            department, courseNumber, courseName, description, units,
            *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        if not self.sections:
            self.sections = []
        self.department = department
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.description = description
        self.units = units


    def __str__(self) -> str:
        # TODO: finish this method
        return f'Department: {self.department}\nCourse number: {self.courseNumber}\nCourse name: {self.courseName}\n' \
               f'Description: {self.description}\nUnits: {self.units}'

    @staticmethod
    def add_document() -> None:
        """
        Create a new Course instance
        :return: None
        """
        success: bool = False
        while not success:
            department = input('Department Abbreviation -->')
            courseNumber = int(input('Course Number -->'))
            courseName = input('Course Name -->')
            description = input('Description -->')
            units = int(input('Units -->'))

            new_course = Course(department, courseNumber, courseName, description, units)
            violated_constraints = unique_general(new_course)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                # Maybe add section so that a course always have atleast 1 section???
                try:
                    new_course.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new department:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        course = Course.select_document()
        if course.sections:
            print('This course has sections attached to it, delete those first and then try again.')
            return
        course.delete()

    @staticmethod
    def list_documents() -> None:
        for course in Course.objects:
            print(course)

    @staticmethod
    def select_document() -> Course:
        return select_general(Course)

    def add_section(self, new_section: Section):
        for section in self.sections:
            if new_section.pk == section.pk:
                return
        self.sections.append(new_section)

    def remove_section(self, old_section: Section):
        for section in self.sections:
            if old_section.pk == section.pk:
                self.sections.remove(old_section)
                return
