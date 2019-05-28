import uuid
from abc import ABCMeta, abstractmethod


class DiscardedEntityException(Exception):
    def __init__(self):
        super().__init__("entity_discarded")


def check_not_discarded(func):
    def wrapper(*args):
        obj = args[0]
        if hasattr(obj, 'discarded') and obj.discarded:
            raise DiscardedEntityException
        return func(*args)
    return wrapper


class Entity(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        self._id = str(uuid.uuid4())
        self._discarded = False

    @property
    def id(self):
        return self._id

    @property
    def discarded(self):
        return self._discarded

    @check_not_discarded
    def discard(self):
        self._discarded = True
