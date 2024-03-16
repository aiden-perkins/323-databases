from utils import Menu, Option

"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the 'action' could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

# The main options for operating on Departments and Courses.
menu_main = Menu('main', 'Please select one of the following options:', [
    Option('Add', 'add()'),
    Option('List', 'list_objects()'),
    Option('Delete', 'delete()'),
    #    Option('Boilerplate Data', 'boilerplate(database)'),
    Option('Exit this application', 'pass')
])

add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option('Department', 'departments.add_department()'),
    #    Option('Course', 'courses.add_course()'),
    #    Option('Major', 'majors.add_major()'),
    Option('Student', 'students.add_student()'),
    #    Option('Student to Major', 'add_student_major()'),
    #    Option('Major to Student', 'add_major_student()'),
    Option('Exit', 'pass')
])

delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    Option('Department', 'departments.delete_department()'),
    #    Option('Course', 'courses.delete_course()'),
    #    Option('Major', 'majors.delete_major()'),
    Option('Student', 'students.delete_student()'),
    #    Option('Student to Major', 'delete_student_major()'),
    #    Option('Major to Student', 'delete_major_student()'),
    Option('Exit', 'pass')
])

list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option('Department', 'departments.list_department()'),
    #    Option('Course', 'courses.list_course()'),
    #    Option('Major', 'majors.list_major()'),
    Option('Student', 'students.list_student()'),
    #    Option('Student to Major', 'list_student_major()'),
    #    Option('Major to Student', 'list_major_student()'),
    Option('Exit', 'pass')
])
