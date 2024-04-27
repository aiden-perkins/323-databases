import logging
import enum

from utils import Menu, Option

Building = enum.Enum('Building', ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'])
Semester = enum.Enum('Semester', ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter'])
Schedule = enum.Enum('Schedule', ['MW', 'TuTh', 'MWF', 'F', 'S'])
Satisfactory = enum.Enum('Satisfactory', ['A', 'B', 'C'])

logging_menu = Menu('debug', 'Please select the logging level from the following:', [
    Option('Debugging', logging.DEBUG),
    Option('Informational', logging.INFO),
    Option('Error', logging.ERROR)
])

main_menu = Menu('main', 'Please select one of the following options:', [
    Option('Add new instance', 'menu_loop(utils.add_menu)'),
    Option('Delete existing instance', 'menu_loop(utils.delete_menu)'),
    Option('List existing instances', 'menu_loop(utils.list_menu)'),
    Option('Select existing instance', 'menu_loop(utils.select_menu)'),
    Option('Exit', 'pass')
])

# options for adding a new instance
add_menu = Menu('add select', 'Which type of object do you want to add?:', [
    Option('Department', 'collection_classes.Department.add_document()'),
    Option('Course', 'collection_classes.Course.add_document()'),
    Option('Major', 'collection_classes.Major.add_document()'),
    Option('Section', 'collection_classes.Section.add_document()'),
    Option('Student', 'collection_classes..add_documenStudentt()'),
    Option('StudentMajor', 'collection_classes.StudentMajor.add_document()'),
    Option('Enrollment', 'collection_classes.Enrollment.add_document()'),
    Option('Letter Grade', 'collection_classes.LetterGrade.add_document()'),
    Option('Pass Fail', 'collection_classes.PassFail.add_document()'),
    Option('Exit', 'pass')
])

# options for deleting an existing instance
delete_menu = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option('Department', 'collection_classes.Department.delete_document()'),
    Option('Course', 'collection_classes.Course.delete_document()'),
    Option('Major', 'collection_classes.Major.delete_document()'),
    Option('Section', 'collection_classes.Section.delete_document()'),
    Option('Student', 'collection_classes.Student.delete_document()'),
    Option('StudentMajor', 'collection_classes.StudentMajor.delete_document()'),
    Option('Enrollment', 'collection_classes.Enrollment.delete_document()'),
    Option('Letter Grade', 'collection_classes.LetterGrade.delete_document()'),
    Option('Pass Fail', 'collection_classes.PassFail.delete_document()'),
    Option('Exit', 'pass')
])

# options for listing the existing instances
list_menu = Menu('list select', 'Which type of object do you want to list?:', [
    Option('Department', 'collection_classes.Department.list_documents()'),
    Option('Course', 'collection_classes.Course.list_documents()'),
    Option('Major', 'collection_classes.Major.list_documents()'),
    Option('Section', 'collection_classes.Section.list_documents()'),
    Option('Student', 'collection_classes.Student.list_documents()'),
    Option('StudentMajor', 'collection_classes.StudentMajor.list_documents()'),
    Option('Enrollment', 'collection_classes.Enrollment.list_documents()'),
    Option('Letter Grade', 'collection_classes.LetterGrade.list_documents()'),
    Option('Pass Fail', 'collection_classes.PassFail.list_documents()'),
    Option('Exit', 'pass')
])

# options for testing the select functions
select_menu = Menu('select select', 'Which type of object do you want to select:', [
    Option('Department', 'print(collection_classes.Department.select_document())'),
    Option('Course', 'print(collection_classes.Course.select_document())'),
    Option('Major', 'print(collection_classes.Major.select_document())'),
    Option('Section', 'print(collection_classes.Section.select_document())'),
    Option('Student', 'print(collection_classes.Student.select_document())'),
    Option('StudentMajor', 'print(collection_classes.StudentMajor.select_document())'),
    Option('Enrollment', 'print(collection_classes.Enrollment.select_document())'),
    Option('Letter Grade', 'print(collection_classes.LetterGrade.select_document())'),
    Option('Pass Fail', 'print(collection_classes.PassFail.select_document())'),
    Option('Exit', 'pass')
])
