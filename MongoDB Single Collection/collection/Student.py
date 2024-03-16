import json

import pymongo


class Student:
    def __init__(self, collection):
        self._students = collection
        student_count = self._students.count_documents({})
        print(f'Students in the collection so far: {student_count}')
        self.create_students_collection()

    def __getattr__(self, item):
        """
        Redirects all function calls that were not found in this class to self._students.
        """
        return getattr(self._students, item)

    def create_students_collection(self):
        students_indexes = self._students.index_information()
        if 'students_last_and_first_names' in students_indexes.keys():
            print('first and last name index present.')
        else:
            self._students.create_index(
                [('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)],
                unique=True,
                name='students_last_and_first_names'
            )
        if 'students_e_mail' in students_indexes.keys():
            print('e-mail address index present.')
        else:
            self._students.create_index([('e_mail', pymongo.ASCENDING)], unique=True, name='students_e_mail')

    def add_student(self):
        """
        Add a new student, making sure that we don't put in any duplicates,
        based on all the candidate keys (AKA unique indexes) on the
        students collection.  Theoretically, we could query MongoDB to find
        the uniqueness constraints in place, and use that information to
        dynamically decide what searches we need to do to make sure that
        we don't violate any of the uniqueness constraints.  Extra credit anyone?
        :return:            None
        """
        # Create a 'pointer' to the students collection within the db database.
        unique_name: bool = False
        unique_email: bool = False
        last_name: str = ''
        first_name: str = ''
        email: str = ''
        while not unique_name or not unique_email:
            last_name = input('Student last name--> ')
            first_name = input('Student first name--> ')
            email = input('Student e-mail address--> ')
            name_count: int = self._students.count_documents({'last_name': last_name, 'first_name': first_name})
            unique_name = name_count == 0
            if not unique_name:
                print('We already have a student by that name.  Try again.')
            if unique_name:
                email_count = self._students.count_documents({'e_mail': email})
                unique_email = email_count == 0
                if not unique_email:
                    print('We already have a student with that e-mail address.  Try again.')
        # Build a new students document preparatory to storing it
        self._students.insert_one({'last_name': last_name, 'first_name': first_name, 'e_mail': email})

    def select_student(self):
        """
        Select a student by the combination of the last and first.
        :return:        The selected student as a dict.  This is not the same as it was
                        in SQLAlchemy, it is just a copy of the Student document from
                        the database.
        """
        # Create a connection to the students collection from this database
        found: bool = False
        last_name: str = ''
        first_name: str = ''
        while not found:
            last_name = input('Student\'s last name--> ')
            first_name = input('Student\'s first name--> ')
            name_count: int = self._students.count_documents({'last_name': last_name, 'first_name': first_name})
            found = name_count == 1
            if not found:
                print('No student found by that name.  Try again.')
        found_student = self._students.find_one({'last_name': last_name, 'first_name': first_name})
        return found_student

    def delete_student(self):
        """
        Delete a student from the database.
        :return:    None
        """
        # student isn't a Student object (we have no such thing in this application)
        # rather it's a dict with all the content of the selected student, including
        # the MongoDB-supplied _id column which is a built-in surrogate.
        student = self.select_student()
        # Create a 'pointer' to the students collection within the db database.
        # student['_id'] returns the _id value from the selected student document.
        deleted = self._students.delete_one({'_id': student['_id']})
        # The deleted variable is a document that tells us, among other things, how
        # many documents we deleted.
        print(f'We just deleted: {deleted.deleted_count} students.')

    def list_student(self):
        """
        List all the students, sorted by last name first, then the first name.
        :return:    None
        """
        # No real point in creating a pointer to the collection, I'm only using it
        # once in here.  The {} inside the find simply tells the find that I have
        # no criteria.  Essentially this is analogous to a SQL find * from students.
        # Each tuple in the sort specification has the name of the field, followed
        # by the specification of ascending versus descending.
        students_collection = self._students.find({}).sort(
            [('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)]
        )
        # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
        for student in students_collection:
            student['_id'] = str(student['_id'])
            print(json.dumps(student, indent=4))
