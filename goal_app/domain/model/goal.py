from abc import ABCMeta, abstractmethod
import uuid
from datetime import datetime


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
        self._progressions = list()

    @property
    def completed(self):
        return self._completed

    @check_not_discarded
    def complete(self):
        self._completed = True

    @property
    def progressions(self):
        return self._progressions

    def add_progression(self, progression: "Progression"):
        self.progressions.append(progression)


class Progression(Entity):

    def __init__(self, note, percentage):
        super().__init__()
        self._note = note
        self._percentage = percentage
        self._datetime = datetime.now()

    @property
    def note(self):
        return self._note

    @property
    def percentage(self):
        return self._percentage
