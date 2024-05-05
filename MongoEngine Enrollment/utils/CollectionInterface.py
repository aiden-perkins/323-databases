import abc

from mongoengine import Document, QuerySetManager


class CombinedMeta(type(Document), type(abc.ABC)):
    pass


class CollectionInterface(Document, abc.ABC, metaclass=CombinedMeta):
    meta = {
        'abstract': True
    }

    # The following attributes are given values elsewhere and are defined here so the annotations can be resolved.
    objects: QuerySetManager
    _fields: list[str]

    """
    I would have liked to just name these methods add, delete, list, and select
    but unfortunately because I am using multiple inheritance, any method in the
    mongoengine.Document class can't be the same name as what I use here, so I
    just append _document(s) to avoid this problem because delete is a method in
    mongoengine.Document.
    """

    @staticmethod
    @abc.abstractmethod
    def add_document() -> None:
        """
        Prompt the user to add a new embedded document.
        """
        raise NotImplementedError('Subclasses need to implement this.')

    @staticmethod
    @abc.abstractmethod
    def delete_document() -> None:
        """
        Prompt the user to delete an embedded document.
        """
        raise NotImplementedError('Subclasses need to implement this.')

    @staticmethod
    @abc.abstractmethod
    def list_documents() -> None:
        """
        Outputs all the objects of the collection.
        """
        raise NotImplementedError('Subclasses need to implement this.')

    @staticmethod
    @abc.abstractmethod
    def select_document():
        """
        Prompt the user to select an embedded document.
        """
        raise NotImplementedError('Subclasses need to implement this.')
