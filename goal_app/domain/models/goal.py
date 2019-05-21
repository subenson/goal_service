from goal_app.domain.models import check_not_discarded, Entity
from goal_app.domain.models.progression import Progression


class Goal(Entity):

    def __init__(self, name, description, due_date):
        super().__init__()
        self._completed = False
        self._name = name
        self._description = description
        self._due_date = due_date
        self._progressions = list()

    @property
    def completed(self):
        return self._completed

    @check_not_discarded
    def complete(self):
        self._completed = True

    @property
    def progressions(self):
        return self._progressions

    def add_progression(self, progression: Progression):
        self.progressions.append(progression)


class GoalFactory:

    def create(self, name, description, due_date):
        return Goal(name=name, description=description, due_date=due_date)
