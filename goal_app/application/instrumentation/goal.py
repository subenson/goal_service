class InMemoryGoalMetrics:

    def __init__(self):
        self.goals_set = 0
        self.goals_completed = 0
        self.goals_discarded = 0

    def new_goal_set(self):
        self.goals_set += 1

    def new_goal_completed(self):
        self.goals_set += 1

    def new_goal_discarded(self):
        self.goals_discarded += 1


class GoalInstrumentation:

    def __init__(self, logger, metrics):
        self.logger = logger
        self.metrics = metrics

    def goal_set(self, goal_id):
        self.metrics.new_goal_set()
        self.logger(f'- Goal Set: {goal_id} '
                    f'(Total: {self.metrics.goals_set})')

    def goal_completed(self, goal_id):
        self.metrics.new_goal_completed()
        self.logger(f'- Goal Completed: {goal_id}'
                    f'(Total: {self.metrics.goals_completed}')

    def goal_discarded(self, goal_id):
        self.metrics.new_goal_discarded()
        self.logger(f'- Goal Discarded: {goal_id}'
                    f'(Total: {self.metrics.goals_discarded}')
