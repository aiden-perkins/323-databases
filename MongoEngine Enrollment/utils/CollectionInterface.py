from __future__ import annotations
import abc


class CollectionInterface(abc.ABC):
    # I would have liked to just name these methods add, delete, list, and select but unfortunately because I am using
    # multiple inheritance, any method in the mongoengine.Document class can't be the same name as what I use here, so
    # I just append _document(s) to avoid this problem because delete is a method in mongoengine.Document.
    @staticmethod
    @abc.abstractmethod
    def add_document(self) -> None:
        raise NotImplementedError('Subclasses need to implement this.')

    @staticmethod
    @abc.abstractmethod
    def delete_document(self) -> None:
        raise NotImplementedError('Subclasses need to implement this.')

    @staticmethod
    @abc.abstractmethod
    def list_documents(self) -> None:
        raise NotImplementedError('Subclasses need to implement this.')

    @staticmethod
    @abc.abstractmethod
    def select_document(self) -> CollectionInterface:
        raise NotImplementedError('Subclasses need to implement this.')
