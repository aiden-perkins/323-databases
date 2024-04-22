from __future__ import annotations

from mongoengine import *

from utils import (Semester, Building, Schedule, prompt_for_enum, unique_general, print_exception, select_general,
                   CollectionInterface)
from collection_classes import Course, Student


class Section(Document, CollectionInterface):
    course = ReferenceField(Course, required=True, reverse_delete_rule=DENY)
    sectionNumber = IntField(db_field='section_number', required=True)
    semester = EnumField(Semester, required=True)
    sectionYear = IntField(db_field='section_year', required=True)
    building = EnumField(Building, required=True)
    room = IntField(db_field='room', min_value=1, max_value=999, required=True)
    schedule = EnumField(Schedule, required=True)
    startTime = IntField(db_field='start_time', min_value=800, max_value=1930, required=True)
    instructor = StringField(db_field='instructor', required=True)

    students = ListField(ReferenceField(Student))

    meta = {
        'collection': 'sections',
        'indexes': [
            {'unique': True, 'fields': ['course', 'sectionNumber', 'semester', 'sectionYear'],
             'name': 'sections_uk_01'},
            {'unique': True, 'fields': ['semester', 'sectionYear', 'building', 'room', 'schedule', 'startTime'],
             'name': 'sections_uk_02'},
            {'unique': True, 'fields': ['semester', 'sectionYear', 'schedule', 'startTime', 'instructor'],
             'name': 'sections_uk_03'}
        ]
    }

    def __init__(
                self,
                sectionNumber: int, semester: Semester, sectionYear: int, building: Building, room: int,
                schedule: Schedule, startTime: int, instructor: str,
                *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        if not self.students:
            self.students = []
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor

    def __str__(self) -> str:
        # TODO: finish this method
        return str(self.sectionNumber)

    @staticmethod
    def add_document() -> None:
        """
        Create a new Section instance.
        :return: None
        """
        success: bool = False
        while not success:
            section_number = int(input('Section number -->'))
            semester = prompt_for_enum('Section semester -->', Semester, 'semester')
            section_year = int(input('Section year -->'))
            building = prompt_for_enum('Section building -->', Building, 'building')
            room = int(input('Section room -->'))
            schedule = prompt_for_enum('Section schedule --> ', Schedule, 'schedule')
            start_time = int(input('Section start time -->'))
            instructor = input('Section instructor')

            new_section = Section(section_number, semester, section_year, building, room, schedule, start_time, instructor)
            violated_constraints = unique_general(new_section)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    new_section.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new section:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        """
        Delete an existing section from the database.
        :return: None
        """
        section = Section.select_document()
        if section.students:
            print('This section has students attached to it, delete those first and then try again.')

    @staticmethod
    def list_documents() -> None:
        for section in Section.objects:
            print(section)

    @staticmethod
    def select_document() -> Section:
        return select_general(Section)

    def add_student(self, new_student: Student) -> None:
        for student in self.students:
            if new_student.pk == student.pk:
                return
        self.students.append(new_student)

    def remove_student(self, old_student: Student) -> None:
        for student in self.students:
            if student.pk == old_student.pk:
                self.students.remove(old_student)
                return
