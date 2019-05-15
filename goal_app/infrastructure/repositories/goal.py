from sqlalchemy.orm.session import Session
from goal_app.domain.model.goal import Goal
from goal_app.domain.port import Repository


class InMemoryGoalRepository(Repository):

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


class SqlAlchemyGoalRepository(Repository):

    def __init__(self, session: Session):
        self._session = session

    def add(self, goal: Goal) -> None:
        self._session.add(goal)

    def get(self, id_) -> Goal:
        return self._session.query(Goal).get(id_)

    def __len__(self) -> int:
        return self._session.query(Goal).count()


