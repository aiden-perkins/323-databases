from sqlalchemy import Table, Time
from sqlalchemy.orm import column_property, Mapped, relationship

from constants import engine, Base
from tables import DepartmentMixin, CourseMixin, SectionMixin


class Department(Base, DepartmentMixin):
    # Creating the Table object does the introspection.  Basically, __table__
    # allows SQLAlchemy to copy the metadata from the Table object into Base.metadata.
    __table__ = Table('departments', Base.metadata, autoload_with=engine)
    # The uniqueness constraint that I explicitly define for the START_OVER approach is already
    # defined, so I don't need it here, so no __table_args__ needed.  The same consideration
    # applies to a foreign key constraint with multiple columns in the parent's primary key.

    # The courses list will not get created just from introspecting the database, so I'm doing that here.
    courses: Mapped[list['Course']] = relationship(back_populates='department')
    # I'm not actually overriding the attribute name here, I just want to see if I can do it.
    # The __table__ attribute refers to the Table object that we created by introspection.
    # More on metadata: https://docs.sqlalchemy.org/en/20/core/metadata.html
    abbreviation: Mapped[str] = column_property(__table__.c.abbreviation)

    def __init__(self, *args):
        """
        This allows me to edit the __init__ instance method of the mixin without having to go to all the other child
        classes and make sure they match up, all the provided arguments are automatically passed
        to the mixin constructor, it can work with **kwargs aswell.
        """
        DepartmentMixin.__init__(self, *args)


class Course(Base, CourseMixin):
    __table__ = Table('courses', Base.metadata, autoload_with=engine)
    sections: Mapped[list['Section']] = relationship(back_populates='course')
    # Otherwise, this property will be named department_abbreviation
    departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
    # This back_populates will not be created by the introspection.
    department: Mapped['Department'] = relationship(back_populates='courses')
    # Otherwise, this property will be named course_number
    courseNumber: Mapped[int] = column_property(__table__.c.course_number)

    def __init__(self, *args):
        """
        This allows me to edit the __init__ instance method of the mixin without having to go to all the other child
        classes and make sure they match up, all the provided arguments are automatically passed
        to the mixin constructor, it can work with **kwargs aswell.
        """
        CourseMixin.__init__(self, *args)


class Section(Base, SectionMixin):
    __table__ = Table('sections', Base.metadata, autoload_with=engine)
    departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
    courseNumber: Mapped[int] = column_property(__table__.c.course_number)
    course: Mapped['Course'] = relationship(back_populates='sections')
    sectionNumber: Mapped[int] = column_property(__table__.c.section_number)
    sectionYear: Mapped[int] = column_property(__table__.c.section_year)
    startTime: Mapped[Time] = column_property(__table__.c.start_time)

    def __init__(self, *args):
        """
        This allows me to edit the __init__ instance method of the mixin without having to go to all the other child
        classes and make sure they match up, all the provided arguments are automatically passed
        to the mixin constructor, it can work with **kwargs aswell.
        """
        SectionMixin.__init__(self, *args)
