# import logging
from datetime import time
from pprint import pprint

from sqlalchemy import and_

from utils import Menu, Option  # , IntrospectionFactory
from utilities import check_unique
from constants import REUSE_NO_INTROSPECTION, START_OVER
from constants import engine, Session, metadata, menu_main, add_menu, delete_menu, list_menu  # , debug_select
from tables import Course, Department, Major, StudentMajor, Student, Section, Enrollment


def add(_session):
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(_session):
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(_session):
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_section(session):
    """
    Prompt the user for the information for a new section and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print('Which course offers this section?')
    course = select_course(session)
    violation = True
    new_section = None
    while violation:
        section_number = int(input('Section number--> '))
        semester = input('Section semester--> ')
        if semester not in ['Fall', 'Spring', 'Winter', 'Summer I', 'Summer II']:
            print('Invalid section. Try again.')
            continue
        section_year = int(input('Section year-->'))
        building = input('Section building-->')
        if building not in ['EC', 'ECS', 'EN2', 'EN3', 'EN4', 'ET', 'SSPA']:
            print('Invalid building. Try again.')
            continue
        room = int(input('Section room-->'))
        schedule = input('Section schedule-->')
        if schedule not in ['MW', 'TuTh', 'MWF', 'F', 'S']:
            print('Invalid schedule. Try again.')
            continue
        start_time = time(*map(int, input('Section start time-->').split(':')))
        instructor = input('Section instructor-->')
        new_section = Section(
            course, section_number, semester, section_year, building, room, schedule, start_time, instructor
        )
        violated_constraints = check_unique(Session, new_section)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(new_section)


def delete_section(session):
    """
    Prompt the user for a section by a combination of things and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print('deleting a section')
    section = select_section(session)
    if len(section.students) > 0:
        print(f'This section has {len(section.students)} students enrolled, unenroll them first then you can delete.')
        return
    session.delete(section)


def select_section(session):
    """
    Prompt the user for a specific section by the combination of department abbreviation, course number,
    section number, semester, and section year.
    :param session:    The connection to the database.
    :return:        The selected department.
    """
    if input('Do you want to use the custom select section (Y/N)? ').lower() == 'y':
        return select_section_custom(session)
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    section_number: int = -1
    semester: str = ''
    section_year: int = -1
    while not found:
        department_abbreviation = input('Section department abbreviation--> ')
        course_number = int(input('Section course number--> '))
        section_number = int(input('Section number--> '))
        semester = input('Section semester--> ')
        if semester not in ['Fall', 'Spring', 'Winter', 'Summer I', 'Summer II']:
            print('Invalid section. Try again.')
            continue
        section_year = int(input('Section year-->'))

        section_count = session.query(Section).filter(
            Section.sectionNumber == section_number, Section.semester == semester, Section.sectionYear == section_year,
            Section.departmentAbbreviation == department_abbreviation, Section.courseNumber == course_number
        ).count()
        found = section_count == 1
        if not found:
            print('No section with that combination. Try again.')
    return_section: Section = session.query(Section).filter(
        Section.sectionNumber == section_number, Section.semester == semester, Section.sectionYear == section_year,
        Section.departmentAbbreviation == department_abbreviation, Section.courseNumber == course_number
    ).first()
    return return_section


def select_section_custom(session):
    sections: [Section] = list(session.query(Section).order_by(Section.courseNumber, Section.sectionNumber))
    for i, section in enumerate(sections):
        print(f'{i + 1}. {section.departmentAbbreviation} {section.courseNumber} {section.sectionNumber}')
    choice = int(input('Which section do you want? ')) - 1
    return sections[choice]


def list_section(session):
    """
    List all sections, sorted by the course number and section.
    :param session:     The connection to the database.
    :return:            None
    """
    sections: [Section] = list(session.query(Section).order_by(Section.courseNumber, Section.sectionNumber))
    for section in sections:
        print(section)


def add_department(session: Session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_building_office: bool = False
    unique_description: bool = False
    name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = -1
    description: str = ''
    while (
        not unique_name or
        not unique_abbreviation or
        not unique_chair_name or
        not unique_building_office or
        not unique_description
    ):
        name = input('Department name--> ')
        abbreviation = input('Department abbreviation--> ')
        chair_name = input('Department chair name--> ')
        building = input('Department building--> ')
        office = int(input('Department office--> '))
        description = input('Department description--> ')

        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print('We already have a department with that name.  Try again.')
            continue
        abbreviation_count: int = session.query(Department).filter(Department.abbreviation == abbreviation).count()
        unique_abbreviation = abbreviation_count == 0
        if not unique_abbreviation:
            print('We already have a department with that abbreviation.  Try again.')
            continue
        chair_name_count: int = session.query(Department).filter(Department.chairName == chair_name).count()
        unique_chair_name = chair_name_count == 0
        if not unique_chair_name:
            print('We already have a department with that chair name.  Try again.')
            continue
        building_office_count: int = session.query(Department).filter(
            Department.building == building, Department.office == office
        ).count()
        unique_building_office = building_office_count == 0
        if not unique_building_office:
            print('We already have a department using that building office.  Try again.')
            continue
        description_count: int = session.query(Department).filter(Department.description == description).count()
        unique_description = description_count == 0
        if not unique_description:
            print('We already have a department with that description.  Try again.')
            continue
    new_department = Department(name, abbreviation, chair_name, building, office, description)
    session.add(new_department)


def add_course_old(session: Session):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print('Which department offers this course?')
    department: Department = select_department(session)
    unique_number: bool = False
    unique_name: bool = False
    number: int = -1
    name: str = ''
    while not unique_number or not unique_name:
        name = input('Course full name--> ')
        number = int(input('Course number--> '))
        name_count: int = session.query(Course).filter(
            Course.departmentAbbreviation == department.abbreviation, Course.name == name
        ).count()
        unique_name = name_count == 0
        if not unique_name:
            print('We already have a course by that name in that department.  Try again.')
        if unique_name:
            number_count = session.query(Course).filter(
                Course.departmentAbbreviation == department.abbreviation, Course.courseNumber == number
            ).count()
            unique_number = number_count == 0
            if not unique_number:
                print('We already have a course in this department with that number.  Try again.')
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    course = Course(department, number, name, description, units)
    session.add(course)


def add_course(session: Session):
    """
    This demonstrates how to use the utilities in SQLAlchemy Utilities for checking
    all the uniqueness constraints of a table in one method call.  The user
    experience is tougher to customize using this technique, but the benefit is that
    new uniqueness constraints will be automatically added to the list to be checked,
    without any change to the add_course code.

    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print('Which department offers this course?')
    department: Department = select_department(session)
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    violation = True  # Flag that we still have to prompt for fresh values
    course = None
    while violation:
        name = input('Course full name--> ')
        number = int(input('Course number--> '))
        course = Course(department, number, name, description, units)
        violated_constraints = check_unique(Session, course)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(course)


def add_major(session: Session):
    """
    Prompt the user for the information for a new major and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print('Which department offers this major?')
    department: Department = select_department(session)
    unique_name: bool = False
    name: str = ''
    while not unique_name:
        name = input('Major name--> ')
        name_count: int = session.query(Major).filter(Major.departmentAbbreviation == department.abbreviation).count()
        unique_name = name_count == 0
        if not unique_name:
            print('We already have a major by that name in that department.  Try again.')
    description: str = input('Please give this major a description -->')
    major: Major = Major(department, name, description)
    session.add(major)


def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    violation = True
    new_student = None
    while violation:
        last_name = input('Student last name--> ')
        first_name = input('Student first name-->')
        email = input('Student e-mail address--> ')
        new_student = Student(last_name, first_name, email)
        violated_constraints = check_unique(Session, new_student)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(new_student)


def add_student_major(session):
    student: Student = select_student(session)
    major: Major = select_major(session)
    student_major_count: int = session.query(StudentMajor).filter(
        StudentMajor.studentId == student.studentID, StudentMajor.majorName == major.name
    ).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print('That student already has that major.  Try again.')
        student = select_student(session)
        major = select_major(session)
    student.add_major(major)
    """The student object instance is mapped to a specific row in the Student table.  But adding
    the new major to its list of majors does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Student's majors list inside of the
    add_major method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_major method.  So instead, I add the student to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this student 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    session.add(student)                           # add the StudentMajor to the session
    session.flush()


def add_student_section(session):
    unique_student_section = False
    student, section = None, None
    while not unique_student_section:
        student = select_student(session)
        section = select_section(session)
        student_section_count: int = session.query(Enrollment).filter(
            Enrollment.studentId == student.studentID,
            Enrollment.departmentAbbreviation == section.departmentAbbreviation,
            Enrollment.courseNumber == section.courseNumber,
            Enrollment.sectionNumber == section.sectionNumber,
            Enrollment.semester == section.semester,
            Enrollment.sectionYear == section.sectionYear,
        ).count()
        unique_student_section: bool = student_section_count == 0
        if not unique_student_section:
            print('That student already has that section.  Try again.')
    student.add_section(section)
    session.add(student)
    session.flush()


def add_major_student(session):
    major: Major = select_major(session)
    student: Student = select_student(session)
    student_major_count: int = session.query(StudentMajor).filter(
        StudentMajor.studentId == student.studentID, StudentMajor.majorName == major.name
    ).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print('That major already has that student.  Try again.')
        major = select_major(session)
        student = select_student(session)
    major.add_student(student)
    """The major object instance is mapped to a specific row in the Major table.  But adding
    the new student to its list of students does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Major's students list inside of the
    add_student method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_student method.  So instead, I add the major to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this major 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    session.add(major)                           # add the StudentMajor to the session
    session.flush()


def add_section_student(session):
    unique_student_section = False
    section, student = None, None
    while not unique_student_section:
        section = select_section(session)
        student = select_student(session)
        student_section_count: int = session.query(Enrollment).filter(
            Enrollment.studentId == student.studentID,
            Enrollment.departmentAbbreviation == section.departmentAbbreviation,
            Enrollment.courseNumber == section.courseNumber,
            Enrollment.sectionNumber == section.sectionNumber,
            Enrollment.semester == section.semester,
            Enrollment.sectionYear == section.sectionYear,
        ).count()
        unique_student_section: bool = student_section_count == 0
        if not unique_student_section:
            print('That section already has that student.  Try again.')
    section.add_student(student)
    session.add(section)
    session.flush()


def select_department(session: Session) -> Department:
    """
    Prompt the user for a specific department by the department abbreviation.
    :param session:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input('Enter the department abbreviation--> ')
        abbreviation_count: int = session.query(Department).filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print('No department with that abbreviation.  Try again.')
    return_department: Department = session.query(Department).filter(Department.abbreviation == abbreviation).first()
    return return_department


def select_course(session: Session) -> Course:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param session:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department_abbreviation = input('Department abbreviation--> ')
        course_number = int(input('Course Number--> '))
        name_count: int = session.query(Course).filter(
            Course.departmentAbbreviation == department_abbreviation, Course.courseNumber == course_number
        ).count()
        found = name_count == 1
        if not found:
            print('No course by that number in that department.  Try again.')
    course = session.query(Course).filter(
        Course.departmentAbbreviation == department_abbreviation, Course.courseNumber == course_number
    ).first()
    return course


def select_student(session) -> Student:
    """
    Select a student by the combination of the last and first.
    :param session:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    last_name: str = ''
    first_name: str = ''
    while not found:
        last_name = input('Student\'s last name--> ')
        first_name = input('Student\'s first name--> ')
        name_count: int = session.query(Student).filter(
            Student.lastName == last_name, Student.firstName == first_name
        ).count()
        found = name_count == 1
        if not found:
            print('No student found by that name.  Try again.')
    student: Student = session.query(Student).filter(
        Student.lastName == last_name, Student.firstName == first_name
    ).first()
    return student


def select_major(session) -> Major:
    """
    Select a major by its name.
    :param session:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    name: str = ''
    while not found:
        name = input('Major\'s name--> ')
        name_count: int = session.query(Major).filter(Major.name == name).count()
        found = name_count == 1
        if not found:
            print('No major found by that name.  Try again.')
    major: Major = session.query(Major).filter(Major.name == name).first()
    return major


def delete_student(session: Session):
    """
    Prompt the user for a student to delete and delete them.
    :param session:     The current connection to the database.
    :return:            None
    """
    student: Student = select_student(session)
    """This is a bit ghetto.  The relationship from Student to StudentMajor has 
    cascade delete, so this delete will work even if a student has declared one
    or more majors.  I could write a method on Student that would return some
    indication of whether it has any children, and use that to let the user know
    that they cannot delete this particular student.  But I'm too lazy at this
    point.
    """
    if len(student.sections) > 0:
        print(f'This student is enrolled in {len(student.sections)} sections, unenroll first then you can delete.')
        return
    session.delete(student)


def delete_department(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print('deleting a department')
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f'Sorry, there are {n_courses} courses in that department.  Delete them first, '
              'then come back here to delete the department.')
    else:
        session.delete(department)


def delete_student_major(session):
    """Undeclare a student from a particular major.
    :param session:    The current database session.
    :return:        None
    """
    print('Prompting you for the student and the major that they no longer have.')
    student: Student = select_student(session)
    major: Major = select_major(session)
    student.remove_major(major)


def delete_student_section(session):
    print('Prompting you for the student and the section that they no longer have.')
    student: Student = select_student(session)
    section: Section = select_section(session)
    if not student.remove_section(section):
        print('Unable to remove that section from that student, they are not enrolled in it.')


def delete_major_student(session):
    """Remove a student from a particular major.
    :param session:    The current database session.
    :return:        None
    """
    print('Prompting you for the major and the student who no longer has that major.')
    major: Major = select_major(session)
    student: Student = select_student(session)
    major.remove_student(student)


def delete_section_student(session):
    print('Prompting you for the section and the student who no longer has that section.')
    section: Section = select_section(session)
    student: Student = select_student(session)
    if not section.remove_student(student):
        print('Unable to remove that student from that section, they are not enrolled in it.')


def list_department(session: Session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_course(session: Session):
    """
    List all courses currently in the database.
    :param session:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = list(session.query(Course).order_by(Course.courseNumber))
    for course in courses:
        print(course)


def list_student(session: Session):
    """
    List all Students currently in the database.
    :param session:    The current connection to the database.
    :return:
    """
    students: [Student] = list(session.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


def list_major(session: Session):
    """
    List all majors in the database.
    :param session:    The current connection to the database.
    :return:
    """
    majors: [Major] = list(session.query(Major).order_by(Major.departmentAbbreviation))
    for major in majors:
        print(major)


def list_student_major(session: Session):
    """Prompt the user for the student, and then list the majors that the student has declared.
    :param session:    The connection to the database
    :return:        None
    """
    student: Student = select_student(session)
    recs = session.query(Student).join(StudentMajor, Student.studentID == StudentMajor.studentId).join(
        Major, StudentMajor.majorName == Major.name).filter(
        Student.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f'Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}')


def list_student_section(session: Session):
    student: Student = select_student(session)
    recs = session.query(Student).join(
        Enrollment, Student.studentID == Enrollment.studentId
    ).join(
        Section, Enrollment.departmentAbbreviation == Section.departmentAbbreviation,
    ).filter(
        Student.studentID == student.studentID,
        Enrollment.departmentAbbreviation == Section.departmentAbbreviation,
        Enrollment.courseNumber == Section.courseNumber,
        Enrollment.sectionNumber == Section.sectionNumber,
        Enrollment.semester == Section.semester,
        Enrollment.sectionYear == Section.sectionYear
    ).add_columns(
        Student.lastName, Student.firstName, Section.courseNumber, Section.sectionNumber
    ).all()
    for stu in recs:
        print(
            f'Student name: {stu.lastName}, {stu.firstName}, Course: {stu.courseNumber}, Section: {stu.sectionNumber}'
        )


def list_section_student(session: Session):
    section: Section = select_section(session)
    recs = session.query(Section).join(
        Enrollment, and_(
            Enrollment.departmentAbbreviation == Section.departmentAbbreviation,
            Enrollment.courseNumber == Section.courseNumber,
            Enrollment.sectionNumber == Section.sectionNumber,
            Enrollment.semester == Section.semester,
            Enrollment.sectionYear == Section.sectionYear
        )
    ).join(
        Student, Enrollment.studentId == Student.studentID
    ).filter(
        Section.departmentAbbreviation == section.departmentAbbreviation,
        Section.courseNumber == section.courseNumber,
        Section.sectionNumber == section.sectionNumber,
        Section.semester == section.semester,
        Section.sectionYear == section.sectionYear,
        Enrollment.studentId == Student.studentID
    ).add_columns(
        Student.lastName, Student.firstName, Section.courseNumber, Section.sectionNumber
    ).all()
    for stu in recs:
        print(
            f'Student name: {stu.lastName}, {stu.firstName}, Course: {stu.courseNumber}, Section: {stu.sectionNumber}'
        )


def list_major_student(session: Session):
    """Prompt the user for the major, then list the students who have that major declared.
    :param session:    The connection to the database.
    :return:        None
    """
    major: Major = select_major(session)
    recs = session.query(Major).join(StudentMajor, StudentMajor.majorName == Major.name).join(
        Student, StudentMajor.studentId == Student.studentID).filter(
        Major.name == major.name).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f'Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}')


def move_course_to_new_department(session: Session):
    """
    Take an existing course and move it to an existing department.  The course has to
    have a department when the course is created, so this routine just moves it from
    one department to another.

    The change in department has to occur from the Course end of the association because
    the association is mandatory.  We cannot have the course not have any department for
    any time the way that we would if we moved it to a new department from the department
    end.

    Also, the change in department requires that we make sure that the course will not
    conflict with any existing courses in the new department by name or number.
    :param session:    The connection to the database.
    :return:        None
    """
    print('Input the course to move to a new department.')
    course = select_course(session)
    old_department = course.department
    print('Input the department to move that course to.')
    new_department = select_department(session)
    if new_department == old_department:
        print('Error, you\'re not moving to a different department.')
    else:
        # check to be sure that we are not violating the {departmentAbbreviation, name} UK.
        name_count: int = session.query(Course).filter(
            Course.departmentAbbreviation == new_department.abbreviation, Course.name == course.name
        ).count()
        unique_name = name_count == 0
        if not unique_name:
            print('We already have a course by that name in that department.  Try again.')
        if unique_name:
            # Make sure that moving the course will not violate the {departmentAbbreviation,
            # course number} uniqueness constraint.
            number_count = session.query(Course).filter(
                Course.departmentAbbreviation == new_department.abbreviation, Course.courseNumber == course.courseNumber
            ).count()
            if number_count != 0:
                print('We already have a course by that number in that department.  Try again.')
            else:
                course.set_department(new_department)


def select_student_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Students.
    :param session:     The connection to the database.
    :return:            None
    """
    # query returns an iterator of Student objects, I want to put those into a list.  Technically,
    # that was not necessary, I could have just iterated through the query output directly.
    students: [Department] = list(session.query(Department).order_by(Department.lastName, Department.firstName))
    options: [Option] = []  # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the 'prompt' and then the student ID (albeit as a string) in as the 'action'.
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Chose a student from this list', options)
    # text_studentId is the 'action' corresponding to the student that the user selected.
    text_student_id: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = session.query(Department).filter(Department.studentId == int(text_student_id)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print('Selected student: ', returned_student)


def list_department_courses(session):
    department = select_department(session)
    dept_courses: [Course] = department.get_courses()
    print('Course for department: ' + str(department))
    for dept_course in dept_courses:
        print(dept_course)


def boilerplate(session):
    """
    Add boilerplate data initially to jump start the testing.  Remember that there is no
    checking of this data, so only run this option once from the console, or you will
    get a uniqueness constraint violation from the database.
    :param session:    The session that's open.
    :return:        None
    """
    department: Department = Department(
        'Computer Engineering Computer Science',
        'CECS',
        'Mehrdad Aliasgari',
        'ECS',
        542,
        'Computer Science and Computer Engineering at CSULB.'
    )
    major1: Major = Major(department, 'Computer Science', 'Fun with blinking lights')
    major2: Major = Major(department, 'Computer Engineering', 'Much closer to the silicon')
    course1 = Course(department, 323, 'Databases', 'SQL, MongoDB, relational', 6)
    course2 = Course(department, 328, 'Algorithms', 'Divide and Conquer, Greedy, NP Complete', 3)
    section1 = Section(course1, 1, 'Fall', 2024, 'VEC', 416, 'MW', time(9), 'David Brown')
    student1: Student = Student('Brown', 'David', 'david.brown@gmail.com')
    student2: Student = Student('Brown', 'Mary', 'marydenni.brown@gmail.com')
    student3: Student = Student('Disposable', 'Bandit', 'disposable.bandit@gmail.com')
    student1.add_major(major1)
    student2.add_major(major1)
    student2.add_major(major2)
    session.add(department)
    session.add(major1)
    session.add(major2)
    session.add(course1)
    session.add(course2)
    session.add(section1)
    session.add(student1)
    session.add(student2)
    session.add(student3)
    session.flush()


def session_rollback():
    """
    Give the user a chance to roll back to the most recent commit point.
    """
    confirm_menu = Menu('main', 'Please select one of the following options:', [
        Option('Yes, I really want to roll back this session', 'sess.rollback()'),
        Option('No, I hit this option by mistake', 'pass')
    ])
    exec(confirm_menu.menu_prompt())


if __name__ == '__main__':
    print('Starting off')
    # logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    # logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    # logging.getLogger('sqlalchemy.engine').setLevel(logging_action)
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging.getLogger('sqlalchemy.pool').setLevel(logging_action)

    # Prompt the user for whether they want to introspect the tables or create all over again.
    # introspection_mode: int = IntrospectionFactory().introspection_type
    introspection_mode: int = 2
    if introspection_mode == START_OVER:
        print('starting over')
        # create the SQLAlchemy structure that contains all the metadata, regardless of the introspection choice.
        metadata.drop_all(bind=engine)  # start with a clean slate while in development

        # Create whatever tables are called for by our 'Entity' classes that we have imported.
        metadata.create_all(bind=engine)
    elif introspection_mode == REUSE_NO_INTROSPECTION:
        print('Assuming tables match class definitions')

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
