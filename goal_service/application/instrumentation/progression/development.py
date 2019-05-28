from goal_service.application.instrumentation.progression.interface import \
    ProgressionInstrumentation
from goal_service.domain.models.goal import Goal
from goal_service.domain.models.progression import Progression


class DevelopmentProgressionInstrumentation(ProgressionInstrumentation):

    def __init__(self, logger, metrics):
        self.logger = logger
        self.metrics = metrics

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

    def progression_lookup_failed(self, progression_id: str):
        self.logger.log(f'- Progression Lookup Failed: {progression_id}')

    def goal_lookup_failed(self, goal_id: str):
        self.logger.log(f'- Goal Lookup Failed: {goal_id}')
