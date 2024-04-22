from __future__ import annotations

from mongoengine import *

from collection_classes import Section, PassFail, LetterGrade


class Enrollment(EmbeddedDocument):
    section = ReferenceField(Section, required=True)
    passFail = EmbeddedDocumentField(PassFail, db_field='pass_fail')
    letterGrade = EmbeddedDocumentField(LetterGrade, db_field='letter_grade')

    meta = {
        'indexes': [
            {'unique': True, 'fields': ['student', 'section'], 'name': 'enrollments_uk_01'},
            {'unique': True, 'fields': ['section.semester', 'section.sectionYear', 'section.course', 'student'],
             'name': 'enrollments_uk_02'}
        ]
    }

    def __init__(self, section: Section, passFail: PassFail, letterGrade: LetterGrade, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.section = section
        self.passFail = passFail
        self.letterGrade = letterGrade

    def __str__(self):
        return ''

    @staticmethod
    def add_document() -> None:
        # TODO: finish this method
        success: bool = False
        while not success:
            section = Section.select_document()
            passFail = PassFail.select_document()
            letterGrade = LetterGrade.select_document()

            new_enrollment = Enrollment(section, passFail, letterGrade)
            violated_constraints = unique_general(new_enrollment)
            if len(violated_constraints) > 0:
                for violated_constraint in violated_constraints:
                    print('Your input values violated constraint: ', violated_constraint)
                print('try again')
            else:
                # TODO: also add a major to the department so a department always has a major.
                try:
                    new_enrollment.save()
                    success = True
                except Exception as e:
                    print('Errors storing the new department:')
                    print(print_exception(e))

    @staticmethod
    def delete_document() -> None:
        # TODO: finish this method
        enrollment = Enrollment.select_document()
        enrollment._instance.delete()  # probably won't work

    @staticmethod
    def list_documents() -> None:
        # TODO: finish this method
        for enrollment in Enrollment.objects:  # probably won't work
            print(enrollment)

    @staticmethod
    def select_document() -> Enrollment:
        # TODO: finish this method
        return select_general(Enrollment)

