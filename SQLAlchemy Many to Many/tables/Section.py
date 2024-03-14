from sqlalchemy import Integer, String, Time, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import Base
from tables import Enrollment, Course


class Section(Base):
    __tablename__ = 'sections'
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10), primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', Integer, nullable=False, primary_key=True)
    course: Mapped[Course] = relationship(back_populates='sections')
    sectionNumber: Mapped[int] = mapped_column('section_number', Integer, nullable=False, primary_key=True)
    semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False, primary_key=True)
    building: Mapped[str] = mapped_column('building', String(6), nullable=False)
    room: Mapped[int] = mapped_column('room', Integer, nullable=False)
    schedule: Mapped[str] = mapped_column('schedule', String(6))
    startTime: Mapped[Time] = mapped_column('start_time', Time)
    instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

    students: Mapped[list[Enrollment]] = relationship(
        back_populates='section', cascade='all, save-update, delete-orphan'
    )

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

    def __init__(
        self, course: Course, section_number, semester, section_year, building, room, schedule, start_time, instructor
    ) -> None:
        self.course = course
        self.departmentAbbreviation = course.departmentAbbreviation
        self.courseNumber = course.courseNumber
        self.sectionNumber = section_number
        self.semester = semester
        self.sectionYear = section_year
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = start_time
        self.instructor = instructor

    def set_course(self, course: Course):
        self.course = course
        self.departmentAbbreviation = course.departmentAbbreviation
        self.courseNumber = course.courseNumber

    def add_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                return
        _enrollment = Enrollment(student, self)

    def remove_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                self.students.remove(next_student)
                return True
        return False

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
