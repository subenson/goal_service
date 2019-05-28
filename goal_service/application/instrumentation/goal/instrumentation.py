from abc import ABC, abstractmethod

from goal_service.domain.models.goal import Goal
from goal_service.domain.models.progression import Progression


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
    def add_progression(self, goal: Goal):
        raise NotImplementedError

    @abstractmethod
    def discard_progression(self, progression: Progression):
        raise NotImplementedError

    @abstractmethod
    def edit_progression(self, progression: Progression):
        raise NotImplementedError

    @abstractmethod
    def goal_lookup_failed(self, goal_id: str, message: str):
        raise NotImplementedError


class DevGoalInstrumentation(GoalInstrumentation):

    def __init__(self, logger, metrics):
        self.logger = logger
        self.metrics = metrics

    def goal_set(self, goal: Goal):
        self.metrics.goal_set()
        self.logger.log(f'- Goal Set: {goal.id} '
                        f'(Total: {self.metrics.goals_set})')

    def goal_completed(self, goal: Goal):
        self.metrics.goal_completed()
        self.logger.log(f'- Goal Completed: {goal.id} '
                        f'(Total: {self.metrics.goals_completed})')

    def goal_discarded(self, goal: Goal):
        self.metrics.goal_discarded()
        self.logger.log(f'- Goal Discarded: {goal.id} '
                        f'(Total: {self.metrics.goals_discarded})')

    def add_progression(self, goal: Goal):
        self.metrics.progression_added()
        self.logger.log(f'- Progression Added to Goal: {goal.id} '
                        f'(Total: {self.metrics.progressions_added})')

    def discard_progression(self, progression: Progression):
        self.metrics.progression_discarded()
        self.logger.log(f'- Progression Discarded: {progression.id} '
                        f'(Total: {self.metrics.progressions_discarded})')

    def edit_progression(self, progression: Progression):
        self.metrics.progression_edited()
        self.logger.log(f'- Progression Edited: {progression.id} '
                        f'(Total: {self.metrics.progressions_edited})')

    def goal_lookup_failed(self, goal_id: str, message: str):
        self.logger.log(f'- Goal Lookup Failed: {goal_id} '
                        f'(Exception: {message})')
