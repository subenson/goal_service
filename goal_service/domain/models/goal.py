from goal_service.domain.models import check_not_discarded, Entity
from goal_service.domain.models.progression import Progression


class Goal(Entity):

    def __init__(self, name, description, due_date):
        super().__init__()
        self._completed = False
        self._name = name
        self._description = description
        self._due_date = due_date
        self._progressions = list()
        self._subgoals = list()

    @property
    def completed(self):
        return self._completed

    @check_not_discarded
    def complete(self):
        self._completed = True

    @property
    def progressions(self):
        return self._progressions

    @check_not_discarded
    def add_progression(self, progression: Progression):
        self.progressions.append(progression)

    @property
    def subgoals(self):
        return self._subgoals

    @check_not_discarded
    def set_subgoal(self, subgoal: "Goal"):
        self.subgoals.append(subgoal)


def create_goal(name, description, due_date):
    return Goal(name=name, description=description, due_date=due_date)
