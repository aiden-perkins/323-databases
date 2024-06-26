import logging
from datetime import time

from lib import Menu, Option, IntrospectionFactory
from constants import menu_main, debug_select, engine, Session, metadata
from constants import START_OVER, INTROSPECT_TABLES, REUSE_NO_INTROSPECTION
from tables import Department, Course, Section


def add_section(session):
    """
    Prompt the user for the information for a new section and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print('Which course offers this section?')
    course = select_course(session)

    unique_primary_key: bool = False
    unique_constraint_1: bool = False
    unique_constraint_2: bool = False

    section_number: int = -1
    semester: str = ''
    section_year: int = -1
    building: str = ''
    room: int = -1
    schedule: str = ''
    start_time: time = time()
    instructor: str = ''

    while not unique_primary_key or not unique_constraint_1 or not unique_constraint_2:
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

        primary_key_count = session.query(Section).filter(
            Section.sectionNumber == section_number, Section.semester == semester, Section.sectionYear == section_year,
            Section.departmentAbbreviation == course.departmentAbbreviation, Section.courseNumber == course.courseNumber
        ).count()
        unique_primary_key = primary_key_count == 0
        if not unique_primary_key:
            print('We already have a section with that '
                  'department abbreviation, course number, section number, semester, and year. Try again.')
            continue

        unique_constraint_1_count = session.query(Section).filter(
            Section.sectionYear == section_year, Section.semester == semester, Section.schedule == schedule,
            Section.startTime == start_time, Section.building == building, Section.room == room
        ).count()
        unique_constraint_1 = unique_constraint_1_count == 0
        if not unique_constraint_1:
            print(
                'We already have a section with that year, semester, schedule, start time, building, & room. Try again.'
            )
            continue

        unique_constraint_2_count = session.query(Section).filter(
            Section.sectionYear == section_year, Section.semester == semester, Section.schedule == schedule,
            Section.startTime == start_time, Section.instructor == instructor
        ).count()
        unique_constraint_2 = unique_constraint_2_count == 0
        if not unique_constraint_2:
            print('We already have a section with that year, semester, schedule, start time, & instructor. Try again.')
            continue

    new_section = Section(
        course, section_number, semester, section_year, building, room, schedule, start_time, instructor
    )
    session.add(new_section)


def add_department(session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_abbreviation: bool = False
    name: str = ''
    abbreviation: str = ''
    while not unique_abbreviation or not unique_name:
        name = input('Department full name--> ')
        abbreviation = input('Department abbreviation--> ')
        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print('We already have a department by that name.  Try again.')
        if unique_name:
            abbreviation_count = session.query(Department).filter(Department.abbreviation == abbreviation).count()
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print('We already have a department with that abbreviation.  Try again.')
    new_department = Department(abbreviation, name)
    session.add(new_department)


def add_course(session):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print('Which department offers this course?')
    department: Department = select_department(sess)
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


def select_section(session):
    """
    Prompt the user for a specific section by the combination of department abbreviation, course number,
    section number, semester, and section year.
    :param session:    The connection to the database.
    :return:        The selected department.
    """
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


def select_department(session) -> Department:
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


def select_course(session) -> Course:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param session:    The connection to the database.
    :return:        The selected course.
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


def delete_section(session):
    """
    Prompt the user for a section by a combination of things and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print('deleting a section')
    section = select_section(session)
    session.delete(section)


def delete_department(session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print('deleting a department')
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f'Sorry, there are {n_courses} courses in that department. '
              f'Delete them first, then come back here to delete the department.')
    else:
        session.delete(department)


def delete_course(session):
    """
    Prompt the user for a course by the combination of things and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print('deleting a course')
    course = select_course(session)
    n_section = session.query(Section).filter(Section.courseNumber == course.courseNumber).count()
    if n_section > 0:
        print(f'Sorry, there are {n_section} sections in that course. '
              f'Delete them first, then come back here to delete the section.')
    else:
        session.delete(course)


def list_sections(session):
    """
    List all sections, sorted by the course number and section.
    :param session:     The connection to the database.
    :return:            None
    """
    sections: [Section] = list(session.query(Section).order_by(Section.courseNumber, Section.sectionNumber))
    for section in sections:
        print(section)


def list_departments(session):
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


def list_courses(session):
    """
    List all courses currently in the database.
    :param session:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = session.query(Course).order_by(Course.courseNumber)
    for course in courses:
        print(course)


def move_course_to_new_department(session):
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
    temp_menu = Menu('Student list', 'From this list, select a student', options)
    # text_studentId is the 'action' corresponding to the student that the user selected.
    text_student_id: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = session.query(Department).filter(Department.studentId == int(text_student_id)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print('Selected student: ', returned_student)


def list_course_sections(session):
    course = select_course(session)
    course_sections: [Section] = course.get_sections()
    print('Sections for course: ' + str(course))
    for course_section in course_sections:
        print(course_section)


def list_department_courses(session):
    department = select_department(session)
    dept_courses: [Course] = department.get_courses()
    print('Course for department: ' + str(department))
    for dept_course in dept_courses:
        print(dept_course)


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
    introspection_mode: int = IntrospectionFactory().introspection_type
    if introspection_mode == START_OVER:
        print('starting over')
        # create the SQLAlchemy structure that contains all the metadata, regardless of the introspection choice.
        metadata.drop_all(bind=engine)  # start with a clean slate while in development

        # Create whatever tables are called for by our 'Entity' classes that we have imported.
        metadata.create_all(bind=engine)
    elif introspection_mode == INTROSPECT_TABLES:
        print('reusing tables')
        # The reflection is done in the imported files that declare the entity classes, so there is no
        # reflection needed at this point, those classes are loaded and ready to go.
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
