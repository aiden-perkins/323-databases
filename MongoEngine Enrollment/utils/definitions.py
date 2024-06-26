import logging
import enum

from utils import Menu, Option

Building = enum.Enum('Building', ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'])
Semester = enum.Enum('Semester', ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter'])
Schedule = enum.Enum('Schedule', ['MW', 'TuTh', 'MWF', 'F', 'S'])
Satisfactory = enum.Enum('Satisfactory', ['A', 'B', 'C'])

logging_menu = Menu('logging', 'Please select the logging level from the following:', [
    Option('Debugging', logging.DEBUG),
    Option('Informational', logging.INFO),
    Option('Error', logging.ERROR)
])

main_menu = Menu('main', 'Please select one of the following options:', [
    Option('Add new instance', 'menu_loop(utils.add_menu)'),
    Option('Delete existing instance', 'menu_loop(utils.delete_menu)'),
    Option('List existing instances', 'menu_loop(utils.list_menu)'),
    Option('Select existing instance', 'menu_loop(utils.select_menu)'),
    Option('Empty database', 'client.drop_database(\'Enrollment\')'),
    Option('Exit', 'pass')
])

# options for adding a new instance
add_menu = Menu('add select', 'Which type of object do you want to add?:', [
    Option('Department', 'collection_documents.Department.add_document()'),
    Option('Course', 'collection_documents.Course.add_document()'),
    Option('Major', 'collection_documents.Major.add_document()'),
    Option('Section', 'collection_documents.Section.add_document()'),
    Option('Student', 'collection_documents.Student.add_document()'),
    Option('StudentMajor', 'collection_documents.StudentMajor.add_document()'),
    Option('Enrollment', 'collection_documents.Enrollment.add_document()'),
    Option('Letter Grade', 'collection_documents.LetterGrade.add_document()'),
    Option('Pass Fail', 'collection_documents.PassFail.add_document()'),
])

# options for deleting an existing instance
delete_menu = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option('Department', 'collection_documents.Department.delete_document()'),
    Option('Course', 'collection_documents.Course.delete_document()'),
    Option('Major', 'collection_documents.Major.delete_document()'),
    Option('Section', 'collection_documents.Section.delete_document()'),
    Option('Student', 'collection_documents.Student.delete_document()'),
    Option('StudentMajor', 'collection_documents.StudentMajor.delete_document()'),
    Option('Enrollment', 'collection_documents.Enrollment.delete_document()'),
    Option('Letter Grade', 'collection_documents.LetterGrade.delete_document()'),
    Option('Pass Fail', 'collection_documents.PassFail.delete_document()'),
])

# options for listing the existing instances
list_menu = Menu('list select', 'Which type of object do you want to list?:', [
    Option('Department', 'collection_documents.Department.list_documents()'),
    Option('Course', 'collection_documents.Course.list_documents()'),
    Option('Major', 'collection_documents.Major.list_documents()'),
    Option('Section', 'collection_documents.Section.list_documents()'),
    Option('Student', 'collection_documents.Student.list_documents()'),
    Option('StudentMajor', 'collection_documents.StudentMajor.list_documents()'),
    Option('Enrollment', 'collection_documents.Enrollment.list_documents()'),
    Option('Letter Grade', 'collection_documents.LetterGrade.list_documents()'),
    Option('Pass Fail', 'collection_documents.PassFail.list_documents()'),
])

# options for testing the select functions
select_menu = Menu('select select', 'Which type of object do you want to select:', [
    Option('Department', 'print(collection_documents.Department.select_document())'),
    Option('Course', 'print(collection_documents.Course.select_document())'),
    Option('Major', 'print(collection_documents.Major.select_document())'),
    Option('Section', 'print(collection_documents.Section.select_document())'),
    Option('Student', 'print(collection_documents.Student.select_document())'),
    Option('StudentMajor', 'print(collection_documents.StudentMajor.select_document())'),
    Option('Enrollment', 'print(collection_documents.Enrollment.select_document())'),
    Option('Letter Grade', 'print(collection_documents.LetterGrade.select_document())'),
    Option('Pass Fail', 'print(collection_documents.PassFail.select_document())'),
])
