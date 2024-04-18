from __future__ import annotations

from mongoengine import *

from utils import Building, CollectionInterface
from collection_classes import Course, Major


class Department(Document, CollectionInterface):
    # TODO: add min/max lengths to these fields, I was lazy and didn't want to open moon modeler
    name = StringField(db_field='name', required=True)
    abbreviation = StringField(db_field='abbreviation', required=True)
    chairName = StringField(db_field='chair_name', required=True)
    building = EnumField(Building, required=True)
    office = IntField(db_field='office', required=True)
    description = StringField(db_field='description', required=True)

    # TODO: confirm that these don't need requirements, I think majors does need at least one
    courses = ListField(ReferenceField(Course))
    majors = ListField(ReferenceField(Major))

    # TODO: add all the uniqueness constraints
    meta = {
        'collection': 'departments',
        'indexes': [
            {'unique': True, 'fields': [''], 'name': 'departments_uk_01'},
        ]
    }

    def __init__(self, name: str, abbreviation: str, chairName: str, building: Building, office: int, description: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not self.courses:
            self.courses = []
        if not self.majors:
            self.majors = []
        self.name = name
        self.abbreviation = abbreviation
        self.chairName = chairName
        self.building = building
        self.office = office
        self.description = description

    def __str__(self) -> str:
        # TODO: finish this method
        return ''

    def add_document(self) -> None:
        # TODO: finish this method
        pass

    def delete_document(self) -> None:
        # TODO: finish this method
        pass

    def list_documents(self) -> None:
        # TODO: finish this method
        pass

    def select_document(self) -> Department:
        # TODO: finish this method
        pass

    def add_major(self, new_major: Major) -> None:
        for major in self.majors:
            if new_major.pk == major.pk:
                return
        self.majors.append(new_major)

    def remove_major(self, old_major: Major) -> None:
        for major in self.majors:
            if major.pk == old_major.pk:
                self.majors.remove(old_major)
                return

    def add_course(self, new_course: Course) -> None:
        for course in self.courses:
            if new_course.pk == course.pk:
                return
        self.courses.append(new_course)

    def remove_course(self, old_course: Course) -> None:
        for course in self.courses:
            if course.pk == old_course.pk:
                self.courses.remove(old_course)
                return
