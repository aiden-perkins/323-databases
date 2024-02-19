from sqlalchemy import String, UniqueConstraint, Integer, ForeignKeyConstraint, Time, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from constants import Base
from tables import DepartmentMixin, CourseMixin, SectionMixin


class Department(Base, DepartmentMixin):
    __tablename__ = 'departments'
    abbreviation: Mapped[str] = mapped_column('abbreviation', String, nullable=False, primary_key=True)
    """This is a bi-directional relationship.  The Department class manages
    a list of Courses, and the Course class manages an OO reference to the
    'owning' Department.

    The Course referenced here is a string because the Course.py file 
    imports Departments.py.  If I try to import Course.py here, I'll set up
    a cyclic import loop and Python will not be able to interpret either of
    those class definition files."""
    courses: Mapped[list['Course']] = relationship(back_populates='department')
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
    # send to the database.  In this case, that we want two separate uniqueness
    # constraints (candidate keys).
    __table_args__ = (UniqueConstraint('name', name='departments_uk_01'),)

    def __init__(self, *args):
        """
        This allows me to edit the __init__ instance method of the mixin without having to go to all the other child
        classes and make sure they match up, all the provided arguments are automatically passed
        to the mixin constructor, it can work with **kwargs aswell.
        """
        DepartmentMixin.__init__(self, *args)


class Course(Base, CourseMixin):
    """A catalog entry.  Each course proposes to offer students who enroll in
    a section of the course an organized sequence of lessons and assignments
    aimed at teaching them specified skills."""
    __tablename__ = 'courses'  # Give SQLAlchemy the name of the table.
    """
    The ForeignKey argument to the mapped_column method is not needed because I am 
    specifying this foreign key constraint in the __table_args__ call farther down
    in the code.  I can do this either 'in-line' using ForeignKey in the mapped_column
    call, OR (exclusive OR here) do it in __table_args__.

    If we have more than one column in the primary key of the parent, then we 
    MUST use __table_args__, we canNOT express the foreign key constraint using
    ForeignKey.  I show you how to do it in __table_args__ because you'll need
    that for the relationship from courses into sections.
    """
    sections: Mapped[list['Section']] = relationship(back_populates='course')
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', primary_key=True)
    department: Mapped['Department'] = relationship(back_populates='courses')
    courseNumber: Mapped[int] = mapped_column('course_number', Integer, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    description: Mapped[str] = mapped_column('description', String(500), nullable=False)
    units: Mapped[int] = mapped_column('units', Integer, nullable=False)
    # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
    # send to the database.  In this case, that we want two separate uniqueness
    # constraints (candidate keys).
    __table_args__ = (
        UniqueConstraint('department_abbreviation', 'name', name='courses_uk_01'),
        ForeignKeyConstraint([departmentAbbreviation], ['departments.abbreviation'])
    )

    def __init__(self, *args):
        """
        This allows me to edit the __init__ instance method of the mixin without having to go to all the other child
        classes and make sure they match up, all the provided arguments are automatically passed
        to the mixin constructor, it can work with **kwargs aswell.
        """
        CourseMixin.__init__(self, *args)


class Section(Base, SectionMixin):
    __tablename__ = 'sections'
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10), primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', Integer, nullable=False, primary_key=True)
    course: Mapped['Course'] = relationship(back_populates='sections')
    sectionNumber: Mapped[int] = mapped_column('section_number', Integer, nullable=False, primary_key=True)
    semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False, primary_key=True)
    building: Mapped[str] = mapped_column('building', String(6), nullable=False)
    room: Mapped[int] = mapped_column('room', Integer, nullable=False)
    schedule: Mapped[str] = mapped_column('schedule', String(6))
    startTime: Mapped[Time] = mapped_column('start_time', Time)
    instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'section_year', 'semester', 'schedule', 'start_time', 'building', 'room', name='sections_uk_01'
        ),
        UniqueConstraint('section_year', 'semester', 'schedule', 'start_time', 'instructor', name='sections_uk_02'),
        ForeignKeyConstraint([departmentAbbreviation], ['departments.abbreviation']),
        ForeignKeyConstraint(
            [departmentAbbreviation, courseNumber], ['courses.department_abbreviation', 'courses.course_number']
        ),
    )

    def __init__(self, *args):
        """
        This allows me to edit the __init__ instance method of the mixin without having to go to all the other child
        classes and make sure they match up, all the provided arguments are automatically passed
        to the mixin constructor, it can work with **kwargs aswell.
        """
        SectionMixin.__init__(self, *args)
