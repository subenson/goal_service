from abc import ABCMeta, abstractmethod
import uuid


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


class Goal(Entity):

    def __init__(self, name, description, due_date):
        super().__init__()
        self._completed = False
        self._name = name
        self._description = description
        self._due_date = due_date

    def complete(self):
        self._completed = True
