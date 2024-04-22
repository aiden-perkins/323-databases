from __future__ import annotations

from mongoengine import *

class LetterGrade(EmbeddedDocument):
    minSatisfactory = StringField(db_field='min_satisfactory', required=True)

    meta = {
        'collection': 'letter_grade'
    }

    def __init__(self, minSatisfactory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minSatisfactory = minSatisfactory

    def __str__(self):
        return ''

    @staticmethod
    def add_document() -> None:
        # TODO: finish this method
        success: bool = False
        while not success:
            minSatisfactory = input('Department Abbreviation -->')

            new_letterGrade = LetterGrade(minSatisfactory)
            violated_constraints = unique_general(new_letterGrade)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                try:
                    new_letterGrade.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new department:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        # TODO: finish this method
        letterGrade = LetterGrade.select_document()
        letterGrade._instance.delete()  # probably won't work

    @staticmethod
    def list_documents() -> None:
        # TODO: finish this method
        for letterGrade in LetterGrade.objects:  # probably won't work
            print(letterGrade)

    @staticmethod
    def select_document() -> LetterGrade:
        # TODO: finish this method
        return select_general(LetterGrade)
