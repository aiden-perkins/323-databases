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
    Option('Add new instance', 'menu_loop(add_menu)'),
    Option('Delete existing instance', 'menu_loop(delete_menu)'),
    Option('List existing instances', 'menu_loop(list_menu)'),
    Option('Select existing instance', 'menu_loop(select_menu)'),
    Option('Exit', 'pass')
])

# options for adding a new instance
add_menu = Menu('add select', 'Which type of object do you want to add?:', [
    # TODO: add the options for all collections
    Option('[Collection]', '[Collection].add()'),
    Option('Exit', 'pass')
])

# options for deleting an existing instance
delete_menu = Menu('delete select', 'Which type of object do you want to delete?:', [
    # TODO: add the options for all collections
    Option('[Collection]', '[Collection].delete()'),
    Option('Exit', 'pass')
])

# options for listing the existing instances
list_menu = Menu('list select', 'Which type of object do you want to list?:', [
    # TODO: add the options for all collections
    Option('[Collection]', '[Collection].list()'),
    Option('Exit', 'pass')
])

# options for testing the select functions
select_menu = Menu('select select', 'Which type of object do you want to select:', [
    # TODO: add the options for all collections
    Option('[Collection]', 'print([Collection].select())'),
    Option('Exit', 'pass')
])
