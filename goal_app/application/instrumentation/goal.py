class InMemoryGoalMetrics:

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


class GoalInstrumentation:

    def __init__(self, logger, metrics):
        self.logger = logger
        self.metrics = metrics

    def goal_set(self, goal_id):
        self.metrics.goal_set()
        self.logger(f'- Goal Set: {goal_id} '
                    f'(Total: {self.metrics.goals_set})')

    def goal_completed(self, goal_id):
        self.metrics.goal_completed()
        self.logger(f'- Goal Completed: {goal_id}'
                    f'(Total: {self.metrics.goals_completed}')

    def goal_discarded(self, goal_id):
        self.metrics.goal_discarded()
        self.logger(f'- Goal Discarded: {goal_id}'
                    f'(Total: {self.metrics.goals_discarded}')

    def add_progression(self, goal_id):
        self.metrics.progression_added()
        self.logger(f'- Progression Added to Goal: {goal_id}'
                    f'(Total: {self.metrics.progressions_added}')

    def discard_progression(self, goal_id):
        self.metrics.progression_discarded()
        self.logger(f'- Progression Discarded: {goal_id}'
                    f'(Total: {self.metrics.progressions_discarded}')

    def edit_progression(self, goal_id):
        self.metrics.progression_edited()
        self.logger(f'- Progression Edited: {goal_id}'
                    f'(Total: {self.metrics.progressions_edited}')
