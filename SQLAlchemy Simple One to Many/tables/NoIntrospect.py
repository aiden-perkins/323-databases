from sqlalchemy import String, UniqueConstraint, Integer, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from constants import Base
from tables import DepartmentMixin, CourseMixin


class DepartmentNoIntrospect(Base, DepartmentMixin):
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

    """The __init__ function appears to be special in SQLAlchemy.  I'm unable to 
    leave that out when the class is initially declared, and then add it in afterwards.
    So I'm defining the exact same __init__ method both for the start over as well
    as the introspection case just to get past this interesting issue and move on."""


class CourseNoIntrospect(Base, CourseMixin):
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
