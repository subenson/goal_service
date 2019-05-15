from sqlalchemy.orm.session import Session
from goal_app.domain.model.goal import Goal, Progression
from goal_app.domain.port import GoalRegistry


class InMemoryGoalRepository(GoalRegistry):

    def __init__(self):
        self._registry = list()

    def add(self, goal: Goal) -> None:
        self._registry.append(goal)

    def get(self, id_) -> Goal:
        for goal in self._registry:
            if goal.id == id_:
                return goal
        return None

    def __len__(self) -> int:
        return len(self._registry)


class InMemoryGoalProgressionRepository(GoalRegistry):

    def __init__(self):
        self._registry = list()

    def add(self, progression: Progression) -> None:
        raise Exception("Unable to add progressions directly in the database.")

    def get(self, id_) -> Progression:
        for progression in self._registry:
            if progression.id == id_:
                return progression
        return None

    def __len__(self) -> int:
        return len(self._registry)


class SqlAlchemyGoalRepository(GoalRegistry):

    def __init__(self, session: Session):
        self._session = session

    def add(self, goal: Goal) -> None:
        self._session.add(goal)

    def get(self, id_) -> Goal:
        return self._session.query(Goal).get(id_)

    def __len__(self) -> int:
        return self._session.query(Goal).count()


class SqlAlchemyGoalProgressionRepository(GoalRegistry):

    def __init__(self, session: Session):
        self._session = session

    def add(self, progression: Progression) -> None:
        raise Exception("Unable to add progressions directly in the database.")

    def get(self, id_) -> Progression:
        return self._session.query(Progression).get(id_)

    def __len__(self) -> int:
        return self._session.query(Progression).count()
