import logging
from configparser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

from utils import Menu, Option

""" constants.py """

START_OVER = 0
# INTROSPECT_TABLES = 1
REUSE_NO_INTROSPECTION = 2

""" db_connection.py """

"""
To get getpass to work properly in PyCharm, you need to configure your project:
Click on the Run Menu at the very top of your PyCharm window.
Select the Edit Configurations menu item.
Select the 'Emulate terminal in output console' checkbox.
This will allow getpass to display the prompt and receive your password in the console.
"""

"""Small utility function whose only job is to manage the connection to the database."""

# This is the URL to my local PostgresSql database.
"""The breakdown of the fields in the URL and what they signify follows:
postgresql -        The relational database dialect.  Note that 'postgres' is no longer 
                    supported by sqlalchemy as a name for this dialect.
psycopg2 -          The database API employed.  It turns out that the default is psycopg2,
                    but I prefer to be explicit.  One less chance of failure.
userID:password     The user credentials used for logging into the database.
host                The name of the 'machine' where PostgreSQL is running.
                    'localhost' signifies that the PostgreSQL instance is running on the
                    same machine where the application is running.
port                The default port # for PostgreSQL is 5432, but I already had a
                    database using that port, so that's why it defaults to 5433.
database            The name of the database within this particular instance of 
                    PostgreSQL.  Every PostgreSQL has a postgres database, but
                    you can create additional databases as needed.  Each CECS 323
                    section has their own database in the campus PostgreSQL instance."""
"""In order to get getpass to prompt you on the console, go to Run | Edit Configurations
in the top menu, and check the box: 'Emulate terminal in output console'.  Otherwise,
you will never see the prompt for the database password."""


"""I'm using a config.ini file that has to be present in the working directory of the 
application.  This seemed a much better solution than prompting for this information
each time that you run the application."""
config = ConfigParser()
config.read('config.ini')               # the config.ini file has to be in the working directory.
userID: str = config['credentials']['userid']
password: str = config['credentials']['password']
host: str = config['credentials']['host']
port: str = config['credentials']['port']
database: str = config['credentials']['database']
# 'psycopg2' in this part of the db_url instructs SQLAlchemy that we are connecting to a PostgreSQL database.
db_url: str = f'postgresql+psycopg2://{userID}:{password}@{host}:{port}/{database}'
db_url_display: str = f'postgresql+psycopg2://{userID}:********@{host}:{port}/{database}'
print('DB URL: ' + db_url_display)
engine = create_engine(db_url, pool_size=5, pool_recycle=3600, echo=False)

session_factory = sessionmaker(bind=engine)
# I am told that this next line contributes to making the code thread safe since the
# scoped_session returns the same Session every time it's called for any given thread.
# I personally don't expect to try to run concurrent threads from Python using
# SQLAlchemy anytime soon, but if I do, I'll be ready!
Session = scoped_session(session_factory)

""" menu_definitions.py """

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
    Option('Add', 'add(sess)'),
    Option('List', 'list_objects(sess)'),
    Option('Delete', 'delete(sess)'),
    Option('Boilerplate Data', 'boilerplate(sess)'),
    Option('Commit', 'sess.commit()'),
    Option('Rollback', 'session_rollback(sess)'),
    Option('Exit this application', 'pass')
])

add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option('Department', 'add_department(sess)'),
    Option('Course', 'add_course(sess)'),
    Option('Section', 'add_section(sess)'),
    Option('Major', 'add_major(sess)'),
    Option('Student', 'add_student(sess)'),
    Option('Student to Major', 'add_student_major(sess)'),
    Option('Major to Student', 'add_major_student(sess)'),
    Option('Student to Section', 'add_student_section(sess)'),
    Option('Section to Student', 'add_section_student(sess)'),
    Option('Exit', 'pass')
])

delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    Option('Department', 'delete_department(sess)'),
    Option('Course', 'delete_course(sess)'),
    Option('Section', 'delete_section(sess)'),
    Option('Major', 'delete_major(sess)'),
    Option('Student', 'delete_student(sess)'),
    Option('Student to Major', 'delete_student_major(sess)'),
    Option('Major to Student', 'delete_major_student(sess)'),
    Option('Student to Section', 'delete_student_section(sess)'),
    Option('Section to Student', 'delete_section_student(sess)'),
    Option('Exit', 'pass')
])

list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option('Department', 'list_department(sess)'),
    Option('Course', 'list_course(sess)'),
    Option('Section', 'list_section(sess)'),
    Option('Major', 'list_major(sess)'),
    Option('Student', 'list_student(sess)'),
    Option('Student to Major', 'list_student_major(sess)'),
    Option('Major to Student', 'list_major_student(sess)'),
    Option('Student to Section', 'list_student_section(sess)'),
    Option('Section to Student', 'list_section_student(sess)'),
    Option('Exit', 'pass')
])

# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', 'Please select a debug level:', [
    Option('Informational', logging.INFO),
    Option('Debug', logging.DEBUG),
    Option('Error', logging.ERROR)
])

# A menu to prompt for whether to create new tables or reuse the old ones.
introspection_select = Menu('introspection selectt', 'To introspect or not:', [
    Option('Start all over', START_OVER),
    # Option('Reuse tables', INTROSPECT_TABLES),
    Option('Reuse without introspection', REUSE_NO_INTROSPECTION)
])

""" orm_base.py """

# Note - The 'connect string' shown in db_connection only goes so far as to specify the
# database name, which defaults to 'postgres' if you just hit enter.   in this case.
# Be sure to create the proper schema in the postgresql database BEFORE trying to run
# this code, SQLAlchemy will not do that for you.
config = ConfigParser()
config.read('config.ini')               # the config.ini file has to be in the working directory.
schema = config['schema']['schema name']
Base = declarative_base(metadata=MetaData(schema=schema))
metadata = Base.metadata
