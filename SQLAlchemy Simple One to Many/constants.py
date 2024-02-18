import os
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

from lib import Menu, Option

load_dotenv()

""" constants.py """

START_OVER = 0
INTROSPECT_TABLES = 1
REUSE_NO_INTROSPECTION = 2

""" orm_base.py """

# Note - The 'connect string' shown in db_connection only goes so far as to specify the
# database name, which defaults to 'postgres' if you just hit enter.   in this case.
# Be sure to create the proper schema in the postgresql database BEFORE trying to run
# this code, SQLAlchemy will not do that for you.

# If nothing is entered when input prompts the user for the schema, then the 'or' gets a
# null string for the first argument which evaluates to false, which means that the
# boolean expression takes the right-hand argument as its output and passes that in to the
# MetaData constructor.

# (input('Schema name [introduction]-->') or 'introduction')
Base = declarative_base(metadata=MetaData(schema=os.getenv('my_id')))
metadata = Base.metadata

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
    Option('Add department', 'add_department(sess)'),
    Option('Add course', 'add_course(sess)'),
    Option('Delete department', 'delete_department(sess)'),
    Option('Delete course', 'delete_course(sess)'),
    Option('List all departments', 'list_departments(sess)'),
    Option('List all courses', 'list_courses(sess)'),
    Option('List department courses', 'list_department_courses(sess)'),
    Option('Move course to new department', 'move_course_to_new_department(sess)'),
    Option('Commit', 'sess.commit()'),
    Option('Break out into shell', 'IPython.embed()'),
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
    Option('Reuse tables', INTROSPECT_TABLES),
    Option('Reuse without introspection', REUSE_NO_INTROSPECTION)
])

""" db_connection.py """

"""
Connection is a module singleton that will create a new connection to the PostgreSQL
database instance.  The connection process will only execute the first time that
you import this module.  In any other language, we would make a class for this
instead, and the object that we return would be a class rather than an instance
variable.  But Python being what it is, we can do this more simply this way.

Note:
To get getpass to work properly in PyCharm, you need to configure your project:
Click on the Run Menu at the very top of your PyCharm window.
Select the Edit Configurations menu item.
Select the 'Emulate terminal in output console' checkbox.
This will allow getpass to display the prompt and receive your password in the console.
"""

# Even though you don't import anything from the psycopg2 package, you still need
# to install it into your SQLAlchemy project.

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
userID: str = 'postgres'  # input('User ID [postgres]--> ') or 'postgres'
"""In order to get getpass to prompt you on the console, go to Run | Edit Configurations
in the top menu, and check the box: 'Emulate terminal in output console'.  Otherwise,
you will never see the prompt for the database password."""

"""If the user simply hits enter when any of these input prompts comes up, the result 
of the input function is a null string, which evaluates to False from a Boolean 
standpoint.  Which then means that the or with a text literal will result in that
literal as the output from the or operator.  Sort of a ghetto way to implement a
default, but it works.  What can I say."""
password: str = os.getenv('db_pass')  # getpass.getpass(prompt=userID + ' password--> ')
host: str = 'localhost'  # input('hostname [localhost]--> ') or 'localhost'
port: str = '5432'  # input('port number [5432]--> ') or '5432'
database: str = 'postgres'  # input('database [postgres]--> ') or 'postgres'
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
