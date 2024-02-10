import logging
from menu_definitions import menu_main, student_select, debug_select, department_select
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Student import Student
from Department import Department
from Option import Option
from Menu import Menu


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


def select_department_name(session: Session) -> Department:
    """
    Prompt the user for a specific department by the name.
    :param session:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    name: str = ''
    while not found:
        name = input('Enter the name--> ')
        name_count: int = session.query(Department).filter(Department.name == name).count()
        found = name_count == 1
        if not found:
            print('No department with that name.  Try again.')
    return_department: Department = session.query(Department).filter(Department.name == name).first()
    return return_department


def select_department_abbreviation(session: Session) -> Department:
    """
    Prompt the user for a specific department by the abbreviation.
    :param session:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input('Enter the abbreviation--> ')
        abbreviation_count: int = session.query(Department).filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print('No department with that abbreviation.  Try again.')
    return_department: Department = session.query(Department).filter(Department.abbreviation == abbreviation).first()
    return return_department


def select_department_chair_name(session: Session) -> Department:
    """
    Prompt the user for a specific department by the chair name.
    :param session:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    chair_name: str = ''
    while not found:
        chair_name = input('Enter the chair name--> ')
        chair_name_count: int = session.query(Department).filter(Department.chairName == chair_name).count()
        found = chair_name_count == 1
        if not found:
            print('No department with that chair name.  Try again.')
    return_department: Department = session.query(Department).filter(Department.chairName == chair_name).first()
    return return_department


def select_department_building_and_office(session: Session) -> Department:
    """
    Prompt the user for a specific department by the building and office.
    :param session:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    building: str = ''
    office: int = -1
    while not found:
        building = input('Enter the building--> ')
        office = int(input('Enter the office--> '))
        building_office_count: int = session.query(Department).filter(
            Department.building == building, Department.office == office
        ).count()
        found = building_office_count == 1
        if not found:
            print('No department with that building and office.  Try again.')
    return_department: Department = session.query(Department).filter(
        Department.building == building, Department.office == office
    ).first()
    return return_department


def select_department_description(session: Session) -> Department:
    """
    Prompt the user for a specific department by the description.
    :param session:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    description: str = ''
    while not found:
        description = input('Enter the description--> ')
        description_count: int = session.query(Department).filter(Department.description == description).count()
        found = description_count == 1
        if not found:
            print('No department with that description.  Try again.')
    return_department: Department = session.query(Department).filter(Department.description == description).first()
    return return_department


def find_department(session: Session) -> Department:
    """
    Prompt the user for attribute values to select a single department.
    :param session:    The connection to the database.
    :return:        The instance of Department that the user selected.
                    Note: there is no provision for the user to simply 'give up'.
    """
    find_department_command = department_select.menu_prompt()
    match find_department_command:
        case 'name':
            old_department = select_department_name(session)
        case 'abbreviation':
            old_department = select_department_abbreviation(session)
        case 'chair name':
            old_department = select_department_chair_name(session)
        case 'building and office':
            old_department = select_department_building_and_office(session)
        case 'description':
            old_department = select_department_description(session)
        case _:
            old_department = None
    return old_department


def delete_department(session: Session):
    """
    Prompt the user for a department by the various attributes and delete that
    department.
    :param session: The connection to the database.
    :return:        None
    """
    print('deleting a department')
    old_department = find_department(session)
    session.delete(old_department)


def list_departments(session: Session):
    """
    List all the departments, sorted by the name.
    :param session:
    :return:
    """
    departments: [Department] = list(session.query(Department).order_by(Department.name))
    for department in departments:
        print(department)


def select_department_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Departments.
    :param session:     The connection to the database.
    :return:            None
    """
    departments: [Department] = list(session.query(Department).order_by(Department.name))
    options: [Option] = []
    for department in departments:
        options.append(Option(f'{department.name} ({department.abbreviation})', department.abbreviation))
    text_abbreviation: str = Menu('Department list', 'Select a department from this list', options).menu_prompt()
    returned_department = session.query(Department).filter(Department.abbreviation == text_abbreviation).first()
    print('Selected department: ', returned_department)


def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    last_name: str = ''
    first_name: str = ''
    email: str = ''
    # Note that there is no physical way for us to duplicate the student_id since we are
    # using the Identity 'type' for studentId and allowing PostgreSQL to handle that.
    # See more at: https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-identity-column/
    while not unique_name or not unique_email:
        last_name = input('Student last name--> ')
        first_name = input('Student first name--> ')
        email = input('Student e-mail address--> ')
        name_count: int = session.query(Student).filter(
            Student.lastName == last_name, Student.firstName == first_name
        ).count()
        unique_name = name_count == 0
        if not unique_name:
            print('We already have a student by that name.  Try again.')
        if unique_name:
            email_count = session.query(Student).filter(Student.eMail == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print('We already have a student with that e-mail address.  Try again.')
    new_student = Student(last_name, first_name, email)
    session.add(new_student)


def select_student_id(session: Session) -> Student:
    """
    Prompt the user for a specific student by the student ID.  Generally
    this is not a terribly useful approach, but I have it here for
    an example.
    :param session:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    student_id: int = -1
    while not found:
        student_id = int(input('Enter the student ID--> '))
        id_count: int = session.query(Student).filter(Student.studentId == student_id).count()
        found = id_count == 1
        if not found:
            print('No student with that ID.  Try again.')
    return_student: Student = session.query(Student).filter(Student.studentId == student_id).first()
    return return_student


def select_student_first_and_last_name(session: Session) -> Student:
    """
    Select a student by the combination of the first and last name.
    :param session:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    last_name: str = ''
    first_name: str = ''
    while not found:
        last_name = input('Student last name to delete--> ')
        first_name = input('Student first name to delete--> ')
        name_count: int = session.query(Student).filter(
            Student.lastName == last_name, Student.firstName == first_name
        ).count()
        found = name_count == 1
        if not found:
            print('No student by that name.  Try again.')
    old_student = session.query(Student).filter(Student.lastName == last_name, Student.firstName == first_name).first()
    return old_student


def select_student_email(session: Session) -> Student:
    """
    Select a student by the e-mail address.
    :param session:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    email: str = ''
    while not found:
        email = input('Enter the student email address --> ')
        id_count: int = session.query(Student).filter(Student.eMail == email).count()
        found = id_count == 1
        if not found:
            print('No student with that email address.  Try again.')
    return_student: Student = session.query(Student).filter(Student.eMail == email).first()
    return return_student


def find_student(session: Session) -> Student:
    """
    Prompt the user for attribute values to select a single student.
    :param session:    The connection to the database.
    :return:        The instance of Student that the user selected.
                    Note: there is no provision for the user to simply 'give up'.
    """
    find_student_command = student_select.menu_prompt()
    match find_student_command:
        case 'ID':
            old_student = select_student_id(session)
        case 'first/last name':
            old_student = select_student_first_and_last_name(session)
        case 'email':
            old_student = select_student_email(session)
        case _:
            old_student = None
    return old_student


def delete_student(session: Session):
    """
    Prompt the user for a student by the last name and first name and delete that
    student.
    :param session: The connection to the database.
    :return:        None
    """
    print('deleting a student')
    old_student = find_student(session)
    session.delete(old_student)


def list_students(session: Session):
    """
    List all the students, sorted by the last name first, then the first name.
    :param session:
    :return:
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    students: [Student] = list(session.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


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
    students: [Student] = list(session.query(Student).order_by(Student.lastName, Student.firstName))
    options: [Option] = []                      # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the 'prompt' and then the student ID (albeit as a string) in as the 'action'.
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the 'action' corresponding to the student that the user selected.
    text_student_id: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = session.query(Student).filter(Student.studentId == int(text_student_id)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print('Selected student: ', returned_student)


if __name__ == '__main__':
    # 6:19:30
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger('sqlalchemy.engine').setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger('sqlalchemy.pool').setLevel(eval(logging_action))

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our 'Entity' classes.
    metadata.create_all(bind=engine)

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
