from goal_service.application.instrumentation.goal.interface import \
    GoalInstrumentation
from goal_service.domain.models.goal import Goal


class DevelopmentGoalInstrumentation(GoalInstrumentation):

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

    def goal_lookup_failed(self, goal_id: str):
        self.logger.log(f'- Goal Lookup Failed: {goal_id}')
