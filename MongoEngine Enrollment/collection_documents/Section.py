from __future__ import annotations

from mongoengine import ReferenceField, IntField, EnumField, StringField, ListField, DENY

import collection_documents
from utils import CollectionInterface
from utils import Semester, Building, Schedule, prompt_for_enum, unique_general, print_exception, select_general


class Section(CollectionInterface):
    course = ReferenceField('Course', required=True, reverse_delete_rule=DENY)
    number = IntField(required=True)
    semester = EnumField(Semester, required=True)
    year = IntField(required=True)
    building = EnumField(Building, required=True)
    room = IntField(min_value=1, max_value=999, required=True)
    schedule = EnumField(Schedule, required=True)
    startTime = IntField(db_field='start_time', min_value=800, max_value=1930, required=True)
    instructor = StringField(required=True)

    students = ListField(ReferenceField('Student'))

    meta = {
        'collection': 'sections',
        'indexes': [
            {
                'unique': True, 'fields': ['course', 'number', 'semester', 'year'],
                'name': 'sections_uk_01'
            },
            {
                'unique': True, 'fields': ['semester', 'year', 'building', 'room', 'schedule', 'startTime'],
                'name': 'sections_uk_02'
            },
            {
                'unique': True, 'fields': ['semester', 'year', 'schedule', 'startTime', 'instructor'],
                'name': 'sections_uk_03'
            }
        ]
    }

    def __str__(self) -> str:
        return f'{self.course}, s{self.number} in the {self.semester.name} of {self.year}'

    @staticmethod
    def add_document() -> None:
        success: bool = False
        while not success:
            print('Select a course: ')
            course = collection_documents.Course.select_document()
            number = int(input('Section number --> '))
            semester = prompt_for_enum('Section semester --> ', Semester)
            year = int(input('Section year --> '))
            building = prompt_for_enum('Section building --> ', Building)
            room = int(input('Section room --> '))
            schedule = prompt_for_enum('Section schedule --> ', Schedule)
            start_time = int(input('Section start time --> '))
            if start_time % 100 >= 60:
                print('That is not a valid start time, try again.')
                continue
            instructor = input('Section instructor --> ')
            new_section = Section(
                course=course, number=number, semester=semester, year=year, building=building, room=room,
                schedule=schedule, startTime=start_time, instructor=instructor
            )
            violated_constraints = unique_general(new_section)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    new_section.save()
                    course.add_section(new_section)
                    course.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new section:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        section = Section.select_document()
        if section.students:
            print('This section has students attached to it, delete those first and then try again.')
            return
        section.course.remove_section(section)
        section.course.save()
        section.delete()

    @staticmethod
    def list_documents() -> None:
        for section in Section.objects().order_by('course', 'number', 'semester', 'year'):
            print(section)

    @staticmethod
    def select_document() -> Section:
        return select_general(Section)

    def add_student(self, new_student: collection_documents.Student) -> None:
        """
        Add a new student to the section.

        :param new_student: The student to be added to the section.
        :return:            None
        """
        for student in self.students:
            if new_student.pk == student.pk:
                return
        self.students.append(new_student)

    def remove_student(self, old_student: collection_documents.Student) -> None:
        """
        Remove an old student from the section if it exists.

        :param old_student: The old student to be removed.
        :return:            None
        """
        for student in self.students:
            if student.pk == old_student.pk:
                self.students.remove(old_student)
                return
