from sqlalchemy.orm.session import Session
from domain.model.goal import Goal
from domain.port import GoalRegistry


class InMemoryGoalRepository(GoalRegistry):

    def __init__(self):
        self._registry = list()

    def add(self, goal: Goal) -> None:
        self._registry.append(goal)

    def get(self, id_):
        raise NotImplementedError

    def __len__(self):
        return len(self._registry)


class SqlAlchemyGoalRepository(GoalRegistry):

    def __init__(self, session: Session):
        self._session = session

    def add(self, goal: Goal) -> None:
        self._session.add(goal)
        self._session.commit()

    def get(self, id_):
        return self._session.query(Goal).get(id_)

    def __len__(self):
        return self._session.query(Goal).count()
