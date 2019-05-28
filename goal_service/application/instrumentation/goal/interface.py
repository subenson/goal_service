from abc import ABC, abstractmethod

from goal_service.domain.models.goal import Goal


class GoalInstrumentation(ABC):

    @abstractmethod
    def goal_set(self, goal: Goal):
        raise NotImplementedError

    @abstractmethod
    def goal_completed(self, goal: Goal):
        raise NotImplementedError

    @abstractmethod
    def goal_discarded(self, goal: Goal):
        raise NotImplementedError

    @abstractmethod
    def goal_lookup_failed(self, goal_id: str):
        raise NotImplementedError
