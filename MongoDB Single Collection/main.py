import os
import json

from pymongo import MongoClient
from dotenv import load_dotenv

from menu_definitions import menu_main, add_menu, delete_menu, list_menu
from collection import Student, Department

load_dotenv()


def add():
    """
    Present the add menu and execute the user's selection.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete():
    """
    Present the delete menu and execute the user's selection.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects():
    """
    Present the list menu and execute the user's selection.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


if __name__ == '__main__':
    # TODO: change to .ini file
    passwd = os.getenv('password')
    username = os.getenv('db_user')
    deployment = os.getenv('deployment')
    cluster_hash = os.getenv('cluster_hash')
    cluster = f'mongodb+srv://{username}:{passwd}@{deployment}.{cluster_hash}.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(cluster)
    print(client.list_database_names())
    database = client['SingleCollection']
    print(database.list_collection_names())

    students = Student(database['students'])
    # I'm using this instead of pprint because I personally think pprint is ugly and harder to read, json.dumps is
    # normally used for writing to config files or storage, but it's also useful here for a clean viewing experience.
    print(json.dumps(students.index_information(), indent=4))

    departments = Department(database['departments'])
    print(json.dumps(departments.index_information(), indent=4))

    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
