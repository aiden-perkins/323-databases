import json

import pymongo
from pymongo import database, errors

import utilities


class Department:
    def __init__(self, collection_name: str, db: database.Database):
        self._name = collection_name
        self._departments = None
        self._database = db
        exisiting_collection = input(f'Do you want to use the exisisting {self._name} collection? (Y/N) ')
        if exisiting_collection.lower() in ['yes', 'y']:
            self._departments = self._database[self._name]
            department_count = self._departments.count_documents({})
            print(f'Departments in the collection so far: {department_count}')
        else:
            self.create_departments_collection()

    def __getattr__(self, item):
        """
        Redirects all function calls that were not found in this class to self._departments.
        """
        return getattr(self._departments, item)

    def create_departments_collection(self):
        validator = {
            '$jsonSchema': {
                'bsonType': 'object',
                'title': 'departments',
                'required': ['name', 'abbreviation', 'chair_name', 'building', 'office', 'description'],
                'properties': {
                    'name': {
                        'bsonType': 'string',
                        'minLength': 10,
                        'maxLength': 50
                    },
                    'abbreviation': {
                        'bsonType': 'string',
                        'maxLength': 6
                    },
                    'chair_name': {
                        'bsonType': 'string',
                        'maxLength': 80
                    },
                    'building': {
                        'enum': ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC']
                    },
                    'office': {
                        'bsonType': 'int'
                    },
                    'description': {
                        'bsonType': 'string',
                        'minLength': 10,
                        'maxLength': 80
                    }
                }
            }
        }
        if self._name in self._database.list_collection_names():
            self._database.drop_collection(self._name)
        self._database.create_collection(self._name, validator=validator)
        self._departments = self._database[self._name]
        departments_indexes = self._departments.index_information()
        if 'departments_name' in departments_indexes.keys():
            print('name index present.')
        else:
            self._departments.create_index([('name', pymongo.ASCENDING)], unique=True, name='departments_name')
        if 'departments_abbreviation' in departments_indexes.keys():
            print('abbreviation index present.')
        else:
            self._departments.create_index(
                [('abbreviation', pymongo.ASCENDING)], unique=True, name='departments_abbreviation'
            )
        if 'departments_chair_name' in departments_indexes.keys():
            print('chair name index present.')
        else:
            self._departments.create_index(
                [('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_name'
            )

        if 'departments_building_office' in departments_indexes.keys():
            print('building and office index present.')
        else:
            self._departments.create_index(
                [('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)], unique=True,
                name='departments_building_office'
            )
        if 'departments_description' in departments_indexes.keys():
            print('description index present.')
        else:
            self._departments.create_index(
                [('description', pymongo.ASCENDING)], unique=True, name='departments_description'
            )

    def add_department(self):
        valid: bool = False
        while not valid:
            name = input('Department name--> ')
            abbreviation = input('Department abbreviation--> ')
            chair_name = input('Department chair name--> ')
            building = input('Department building--> ')
            office = int(input('Department office--> '))
            description = input('Department description--> ')

            try:
                document = {
                    'name': name,
                    'abbreviation': abbreviation,
                    'chair_name': chair_name,
                    'building': building,
                    'office': office,
                    'description': description
                }
                utilities.check_all_unique(self._departments, document)
                self._departments.insert_one(document)
                valid = True
            except (errors.WriteError, errors.DuplicateKeyError) as exception:
                print(utilities.print_exception(exception))

    def select_department(self):
        found: bool = False
        name: str = ''
        while not found:
            name = input('Department name--> ')
            name_count: int = self._departments.count_documents({'name': name})
            found = name_count == 1
            if not found:
                print('No department found by that name.  Try again.')
        found_department = self._departments.find_one({'name': name})
        return found_department

    def delete_department(self):
        department = self.select_department()
        deleted = self._departments.delete_one({'_id': department['_id']})
        print(f'We just deleted: {deleted.deleted_count} departments.')

    def list_department(self):
        departments_collection = self._departments.find({}).sort([('name', pymongo.ASCENDING)])
        for department in departments_collection:
            department['_id'] = str(department['_id'])
            print(json.dumps(department, indent=4))
