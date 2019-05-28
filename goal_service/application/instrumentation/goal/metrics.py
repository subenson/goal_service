from abc import ABC, abstractmethod


class GoalMetrics(ABC):

    @abstractmethod
    def goal_set(self):
        raise NotImplementedError

    @abstractmethod
    def goal_completed(self):
        raise NotImplementedError

    @abstractmethod
    def goal_discarded(self):
        raise NotImplementedError


class InMemoryGoalMetrics(GoalMetrics):

    def __init__(self):
        self.goals_set = 0
        self.goals_completed = 0
        self.goals_discarded = 0

    def goal_set(self):
        self.goals_set += 1

    def goal_completed(self):
        self.goals_set += 1

    def goal_discarded(self):
        self.goals_discarded += 1
