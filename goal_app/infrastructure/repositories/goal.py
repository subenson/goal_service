from sqlalchemy.orm.session import Session
from goal_app.domain.models.goal import Goal
from goal_app.domain.port import Repository
from goal_app.infrastructure.repositories import EntityNotFoundException


class InMemoryGoalRepository(Repository):

    def __init__(self):
        self._registry = list()

    def add(self, goal: Goal) -> None:
        self._registry.append(goal)

    def get(self, id_) -> Goal:
        for goal in self._registry:
            if goal.id == id_:
                return goal
        raise EntityNotFoundException

    def __len__(self) -> int:
        return len(self._registry)


class SqlAlchemyGoalRepository(Repository):

    def __init__(self, session: Session):
        self._session = session

    def add(self, goal: Goal) -> None:
        self._session.add(goal)

    def get(self, id_) -> Goal:
        goal = self._session.query(Goal).get(id_)
        if goal:
            return goal
        raise EntityNotFoundException

    def __len__(self) -> int:
        return self._session.query(Goal).count()


