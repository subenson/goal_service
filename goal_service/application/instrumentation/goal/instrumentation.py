from abc import ABC, abstractmethod


class GoalInstrumentation(ABC):

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
    def add_progression(self, goal):
        raise NotImplementedError

    @abstractmethod
    def discard_progression(self, goal):
        raise NotImplementedError

    @abstractmethod
    def edit_progression(self, goal):
        raise NotImplementedError


class DevGoalInstrumentation(GoalInstrumentation):

    def __init__(self, logger, metrics):
        self.logger = logger
        self.metrics = metrics

    def goal_set(self, goal):
        self.metrics.goal_set()
        self.logger.log(f'- Goal Set: {goal.id} '
                        f'(Total: {self.metrics.goals_set})')

    def goal_completed(self, goal):
        self.metrics.goal_completed()
        self.logger.log(f'- Goal Completed: {goal.id} '
                        f'(Total: {self.metrics.goals_completed})')

    def goal_discarded(self, goal):
        self.metrics.goal_discarded()
        self.logger.log(f'- Goal Discarded: {goal.id} '
                        f'(Total: {self.metrics.goals_discarded})')

    def add_progression(self, goal):
        self.metrics.progression_added()
        self.logger.log(f'- Progression Added to Goal: {goal.id} '
                        f'(Total: {self.metrics.progressions_added})')

    def discard_progression(self, progression):
        self.metrics.progression_discarded()
        self.logger.log(f'- Progression Discarded: {progression.id} '
                        f'(Total: {self.metrics.progressions_discarded})')

    def edit_progression(self, progression):
        self.metrics.progression_edited()
        self.logger.log(f'- Progression Edited: {progression.id} '
                        f'(Total: {self.metrics.progressions_edited})')
