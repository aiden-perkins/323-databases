from sqlalchemy import ForeignKey, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import Base


class Enrollment(Base):
    __tablename__ = 'enrollments'

    student: Mapped['Student'] = relationship(back_populates='sections')
    studentId: Mapped[int] = mapped_column('student_id', ForeignKey('students.student_id'), primary_key=True)

    section: Mapped['Section'] = relationship(back_populates='students')
    departmentAbbreviation: Mapped[str] = mapped_column(
        'department_abbreviation', primary_key=True
    )
    courseNumber: Mapped[int] = mapped_column('course_number', primary_key=True)
    sectionNumber: Mapped[int] = mapped_column('section_number', primary_key=True)
    semester: Mapped[str] = mapped_column('semester', primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year', primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint([studentId], ['students.student_id']),
        ForeignKeyConstraint(
            [departmentAbbreviation, courseNumber, sectionNumber, semester, sectionYear],
            [
                'sections.department_abbreviation', 'sections.course_number',
                'sections.section_number', 'sections.semester', 'sections.section_year'
            ]
        ),
        UniqueConstraint(
            'department_abbreviation', 'course_number', 'section_year', 'semester', 'student_id',
            name='enrollments_uk_01'
        ),
    )

    def __init__(self, student, section):
        self.student = student
        self.studentId = student.studentID
        self.section = section
        self.departmentAbbreviation = section.departmentAbbreviation
        self.courseNumber = section.courseNumber
        self.sectionNumber = section.sectionNumber
        self.semester = section.semester
        self.sectionYear = section.sectionYear

    def __str__(self):
        return f'Enrollment - student: {self.student} section: {self.section}'
