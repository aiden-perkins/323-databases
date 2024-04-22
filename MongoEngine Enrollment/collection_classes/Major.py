from __future__ import annotations

from mongoengine import *

from utils import unique_general, print_exception, select_general, CollectionInterface
from collection_classes import Department


class Major(Document, CollectionInterface):
    department = ReferenceField(Department, required=True, reverse_delete_rule=DENY)
    name = StringField(db_field='name', required=True)
    description = StringField(db_field='description', required=True)

    meta = {
        'collection': 'majors',
        'indexes': [
            {'unique': True, 'fields': ['name'], 'name': 'majors_uk_01'},
        ]
    }

    def __init__(
                self,
                name: str, description: str,
                *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.name = name
        self.description = description

    def __str__(self) -> str:
        # TODO: finish this method
        return self.name

    @staticmethod
    def add_document() -> None:
        """
        Create a new Major instance.
        :return: None
        """
        success: bool = False
        while not success:
            name = input('Major name --> ')
            description = input('Major description -->')

            new_major = Major(name, description)
            violated_constraints = unique_general(new_major)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    new_major.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new major:')
                    print(print_exception(e))


    @staticmethod
    def delete_document() -> None:
        """
        Delete an existing major from the database.
        :return: None
        """
        major = Major.select_document()
        major.delete()

    @staticmethod
    def list_documents() -> None:
        for major in Major.objects:
            print(major)

    @staticmethod
    def select_document() -> Major:
        return select_general(Major)
