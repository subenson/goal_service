from abc import ABC, abstractmethod

from goal_service.domain.models.goal import Goal
from goal_service.domain.models.progression import Progression


class ProgressionInstrumentation(ABC):

    @abstractmethod
    def add_progression(self, goal: Goal):
        raise NotImplementedError

    @abstractmethod
    def discard_progression(self, progression: Progression):
        raise NotImplementedError

    @abstractmethod
    def edit_progression(self, progression: Progression):
        raise NotImplementedError

    @abstractmethod
    def progression_lookup_failed(self, progression_id: str):
        raise NotImplementedError

    @abstractmethod
    def goal_lookup_failed(self, goal_id: str):
        raise NotImplementedError
