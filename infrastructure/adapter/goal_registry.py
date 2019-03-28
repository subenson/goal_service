from sqlalchemy.orm.session import Session
from domain.model.goal import Goal
from domain.port import GoalRegistry


class InMemoryGoalRegistry(GoalRegistry):

    def __init__(self):
        self._registry = list()

    def add(self, goal: Goal) -> None:
        self._registry.append(goal)

    def __len__(self):
        return len(self._registry)


class SqlAlchemyGoalRegistry(GoalRegistry):

    def __init__(self, session: Session):
        self._session = session

    def add(self, goal: Goal) -> None:
        self._session.add(goal)
        self._session.commit()

    def __len__(self):
        return self._session.query(Goal).count()
