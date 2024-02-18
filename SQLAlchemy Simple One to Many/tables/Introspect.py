from sqlalchemy import Table
from sqlalchemy.orm import column_property, Mapped, relationship

from constants import engine, Base
from tables import DepartmentMixin, CourseMixin


class DepartmentIntrospect(Base, DepartmentMixin):
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


class CourseIntrospect(Base, CourseMixin):
    __table__ = Table('courses', Base.metadata, autoload_with=engine)
    # Otherwise, this property will be named department_abbreviation
    departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
    # This back_populates will not be created by the introspection.
    department: Mapped['Department'] = relationship(back_populates='courses')
    # Otherwise, this property will be named course_number
    courseNumber: Mapped[int] = column_property(__table__.c.course_number)
