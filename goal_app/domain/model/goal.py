from abc import ABCMeta, abstractmethod
import uuid


class DiscardedEntityException(Exception):
    def __init__(self):
        super().__init__("entity_discarded")


def check_not_discarded(func):
    def wrapper(*args):
        obj = args[0]
        if hasattr(obj, '_discarded') and obj._discarded:
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


class Goal(Entity):

    def __init__(self, name, description, due_date):
        super().__init__()
        self._completed = False
        self._name = name
        self._description = description
        self._due_date = due_date

    @property
    def completed(self):
        return self._completed

    @check_not_discarded
    def complete(self):
        self._completed = True
