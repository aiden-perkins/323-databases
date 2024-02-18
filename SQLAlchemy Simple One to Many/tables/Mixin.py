from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


class DepartmentMixin:
    @declared_attr
    def courses(self):
        return relationship('Course', back_populates='department')

    def __init__(self, abbreviation: str, name: str):
        self.abbreviation = abbreviation
        self.name = name

    def add_course(self, course):
        if course not in self.courses:
            self.courses.add(course)  # I believe this will update the course as well.

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def get_courses(self):
        return self.courses

    def __str__(self):
        return (f'Department abbreviation: {self.abbreviation} '
                f'name: {self.name} number course offered: {len(self.courses)}')


class CourseMixin:
    def __init__(self, department: 'Department', courseNumber: int, name: str, description: str, units: int):
        self.department = department
        self.departmentAbbreviation = department.abbreviation
        self.courseNumber = courseNumber
        self.name = name
        self.description = description
        self.units = units

    def set_department(self, department: 'Department'):
        """
        Accept a new department withoug checking for any uniqueness.
        I'm going to assume that either a) the caller checked that first
        and/or b) the database will raise its own exception.
        :param department:  The new department for the course.
        :return:            None
        """
        self.department = department
        self.departmentAbbreviation = department.abbreviation

    def __str__(self):
        return (f'Department abbrev: {self.departmentAbbreviation} '
                f'number: {self.courseNumber} name: {self.name} units: {self.units}')
