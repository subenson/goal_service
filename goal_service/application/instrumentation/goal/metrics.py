from abc import ABC, abstractmethod


class GoalMetrics(ABC):

    @abstractmethod
    def goal_set(self, goal):
        raise NotImplementedError

    @abstractmethod
    def goal_completed(self, goal):
        raise NotImplementedError

    @abstractmethod
    def goal_discarded(self, goal):
        raise NotImplementedError

    @abstractmethod
    def progression_added(self, goal):
        raise NotImplementedError

    @abstractmethod
    def progression_discarded(self, goal):
        raise NotImplementedError

    @abstractmethod
    def progression_edited(self, goal):
        raise NotImplementedError


class InMemoryGoalMetrics(GoalMetrics):

    def __init__(self):
        self.goals_set = 0
        self.goals_completed = 0
        self.goals_discarded = 0
        self.progressions_added = 0
        self.progressions_discarded = 0
        self.progressions_edited = 0

    def goal_set(self):
        self.goals_set += 1

    def goal_completed(self):
        self.goals_set += 1

    def goal_discarded(self):
        self.goals_discarded += 1

    def progression_added(self):
        self.progressions_added += 1

    def progression_discarded(self):
        self.progressions_discarded += 1

    def progression_edited(self):
        self.progressions_edited += 1
