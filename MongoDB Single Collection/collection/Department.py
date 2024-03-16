import json

import pymongo


class Department:
    def __init__(self, collection):
        self._departments = collection
        department_count = self._departments.count_documents({})
        print(f'Departments in the collection so far: {department_count}')
        self.create_departments_collection()

    def __getattr__(self, item):
        """
        Redirects all function calls that were not found in this class to self._departments.
        """
        return getattr(self._departments, item)

    def create_departments_collection(self):
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

            name_count: int = self._departments.count_documents({'name': name})
            unique_name = name_count == 0
            if not unique_name:
                print('We already have a department by that name.  Try again.')
                continue

            abbreviation_count = self._departments.count_documents({'abbreviation': abbreviation})
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print('We already have a department with that abbreviation.  Try again.')
                continue

            chair_name_count = self._departments.count_documents({'chair_name': chair_name})
            unique_chair_name = chair_name_count == 0
            if not unique_chair_name:
                print('We already have a department with that chair name.  Try again.')
                continue

            building_office_count = self._departments.count_documents({'building': building, 'office': office})
            unique_building_office = building_office_count == 0
            if not unique_building_office:
                print('We already have a department with that building office.  Try again.')
                continue

            description_count = self._departments.count_documents({'description': description})
            unique_description = description_count == 0
            if not unique_description:
                print('We already have a department with that description.  Try again.')
                continue

        self._departments.insert_one({
            'name': name,
            'abbreviation': abbreviation,
            'chair_name': chair_name,
            'building': building,
            'office': office,
            'description': description
        })

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
