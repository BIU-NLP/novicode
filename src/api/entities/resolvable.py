from __future__ import annotations
from abc import abstractclassmethod, abstractmethod
from typing import TypeVar, Generic, Optional, Union, List
import numpy as np
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from entities.entity import Entity
from exceptions.exceptions import exception_handler
from providers.data_model import DataModel
from utils.lang_utils import compute_bleu_score

nltk.download('punkt')
nltk.download('stopwords')

T = TypeVar("T", bound="Resolvable")


class Resolvable(Generic[T]):
    """
    The Resolvable class is the base class for all resolvable entities.
    Resolvable entities are used to represent parameters in the API.
    This class bridges the user intent expressed in natural language and expected objects in the API.
    For exmaple, Contact, Location, DateTime, etc. are all resolvable entities.
    Resolvable objects are resolve from the user input or from entities recieved from the API.
    """

    # @exception_handler
    @classmethod
    def resolve_from_text(T, text: str) -> T:
        """
        This class method resolves a resolvable object from the user input.
        The resolved text will usually be a phrase within the user instruction.
        For exmaple:
            * "To San Francisco" will resolve to a Location object.
            * "After 8PM" will resolve to a DateTime object.
            * "To my cousin John" will resolve to a Contact object.

        Parameters
        ----------
        text : str
            The text to recover a Resolvable object from

        Returns
        -------
        T
            The resolable template object that is calling this method
        """
        data_model = DataModel()
        data = data_model.get_data(T)
        if data is None:
            raise NotImplementedError()

        items = [
            x
            for x in data
            if hasattr(x, "text") and compute_bleu_score(text, x.text) > 0.333
        ]

        if len(items) == 0:
            if os.environ.get("TEST_RESOLVE_FAIL", False):
                raise ValueError()
            else:
                return None
        else:
            max_index = np.argmax([compute_bleu_score(text, x.text) for x in items])
            result = items[max_index]
            return result

    @classmethod
    def resolve_many_from_text(T, text: str) -> List[T]:
        """
        This class method resolves a list of resolvable object from the user input.
        The resolved text will usually be a phrase within the user instruction. Resolve from many will usually
        include a plural form of a noun. Alternatively, it will include a singular noun with a semantics of plural.
        For example:
            * "Every store in 10 miles radius" will resolve to a list Location objects.
            * "The weekend" will be resolved to a list of DateTime objects.
            * "My book reading club" will resolve to a list Contact object.

        Parameters
        ----------
        text : str
            The text to recover a list of Resolvable objects from

        Returns
        -------
        List[T]
            The resolable template object that is calling this method
        """
        data_model = DataModel()
        data = data_model.get_data(T)
        if data is None:
            raise NotImplementedError()

        # items = [
        #     x for x in data if x.text == text
        # ]  # when resolved many from text we expect the text to be a substring of the actual text

        items = [
            x
            for x in data
            if hasattr(x, "text") and compute_bleu_score(text, x.text) > 0.333
        ]

        if len(items) == 0:
            if os.environ.get("TEST_RESOLVE_FAIL", False):
                raise ValueError()
            else:
                return []
        else:
            result = items
            return result

    # @exception_handler
    @classmethod
    def resolve_from_entity(
        T,
        entity: Union[Entity, List[Entity]],
        text: Optional[str] = None,
    ) -> T:
        """
        This class method resolves a resolvable object from an entity object.
        It is possible that we would like to resolve a one resolvable object from another resolvable object.
        This scenario is typical when using a result of a previous API call as a parameter for a subsequent API call.
        For example:
            * "find directions to San Francisco and send them to John". The navigation directions result will be resolved
            to a Content object in the subsequent API call to send a message.
            * "Find the nearest open pharmacy and navigate to it". The map object will be resolve to a Location object
            in the subsequent API call to navigate to it.

        Parameters
        ----------
        entity : Entity
            The entity object to recover a Resolvable object from

        Returns
        -------
        T
            The resolable template object that is calling this method
        """
        data_model = DataModel()
        clazz = entity[0].__class__ if isinstance(entity, list) else entity.__class__
        data = data_model.get_data(clazz)
        if data is None:
            raise NotImplementedError()

        entities = [
            x
            for x in data
            if ((isinstance(entity, list) and x in entity) or (x == entity))
        ]
        items = (
            [T(value=entity) for entity in entities]
            if not isinstance(entity, list)
            else [T(value=[entity]) for entity in entity]
        )

        if text:
            items = [
                x
                for x in data
                if hasattr(x, "text") and compute_bleu_score(text, x.text) > 0.333
            ]

        if len(items) == 0:
            if os.environ.get("TEST_RESOLVE_FAIL", False):
                raise ValueError()
            else:
                return None
        else:
            result = items[0]
            return result


