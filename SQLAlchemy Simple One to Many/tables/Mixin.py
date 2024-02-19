from datetime import time

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


class DepartmentMixin:
    @declared_attr
    def courses(self):
        return relationship('Course', back_populates='department')

    def __init__(self, abbreviation: str, name: str):
        self.abbreviation = abbreviation
        self.name = name

    def get_courses(self):
        return self.courses

    def __str__(self):
        return (f'Department abbreviation: {self.abbreviation} '
                f'name: {self.name} number course offered: {len(self.courses)}')


class CourseMixin:
    @declared_attr
    def sections(self):
        return relationship('Section', back_populates='course')

    def __init__(self, department: 'Department', courseNumber: int, name: str, description: str, units: int) -> None:
        self.department = department
        self.departmentAbbreviation = department.abbreviation
        self.courseNumber = courseNumber
        self.name = name
        self.description = description
        self.units = units

    def set_department(self, department: 'Department') -> None:
        """
        Accept a new department withoug checking for any uniqueness.
        I'm going to assume that either a) the caller checked that first
        and/or b) the database will raise its own exception.
        :param department:  The new department for the course.
        :return:            None
        """
        self.department = department
        self.departmentAbbreviation = department.abbreviation

    def get_sections(self):
        return self.sections

    def __str__(self) -> str:
        return (f'Department abbrev: {self.departmentAbbreviation} '
                f'number: {self.courseNumber} name: {self.name} units: {self.units}')


class SectionMixin:
    def __init__(
            self, course: 'Course', sectionNumber: int, semester: str, sectionYear: int,
            building: str, room: int, schedule: str, startTime: time, instructor: str
    ) -> None:
        self.course = course
        self.departmentAbbreviation = course.departmentAbbreviation
        self.courseNumber = course.courseNumber
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor

    def set_course(self, course: 'Course'):
        self.course = course
        self.departmentAbbreviation = course.departmentAbbreviation
        self.courseNumber = course.courseNumber

    def __str__(self) -> str:
        output = f'Department abbreviation: {self.departmentAbbreviation}\n'
        output += f'Course number: {self.courseNumber}\n'
        output += f'Section: {self.sectionNumber}\n'
        output += f'Semester: {self.semester} {self.sectionYear}\n'
        output += f'Building: {self.building}\n'
        output += f'Room: {self.room}\n'
        output += f'Schedule: {self.schedule}\n'
        output += f'Instructor: {self.instructor}'
        return output
