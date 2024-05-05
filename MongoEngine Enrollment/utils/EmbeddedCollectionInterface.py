from __future__ import annotations
import abc
from typing import Iterator

from mongoengine import EmbeddedDocument

from utils import CollectionInterface


class CombinedMeta(type(EmbeddedDocument), type(abc.ABC)):
    pass


class EmbeddedCollectionInterface(EmbeddedDocument, abc.ABC, metaclass=CombinedMeta):
    meta = {
        'abstract': True
    }

    _meta: dict
    _fields: list[str]

    @abc.abstractmethod
    def get_parent(self) -> EmbeddedCollectionInterface | CollectionInterface:
        """
        Get the parent object of the embedded object. This can sometimes also
        be an embedded document so DO NOT use this to try and get the collection
        where the embedded object is stored.

        :return: The parent collection object.
        """
        raise NotImplementedError('Subclasses need to implement this.')

    @abc.abstractmethod
    def get_document(self) -> CollectionInterface:
        """
        Get the document of the embedded object. This should always be used
        instead of get_parent whenever possible.

        :return: The parent document object.
        """
        raise NotImplementedError('Subclasses need to implement this.')

    @staticmethod
    @abc.abstractmethod
    def get_all_objects() -> Iterator[EmbeddedCollectionInterface]:
        """
        Get all the objects belonging to an Embedded Collection.

        :return: A generator that yields all objects of the class.
        """
        raise NotImplementedError('Subclasses need to implement this.')

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
