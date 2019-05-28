from sqlalchemy.orm.session import Session
from goal_service.domain.models.goal import Goal
from goal_service.domain.port import Repository
from goal_service.infrastructure.repositories import EntityNotFoundException


class InMemoryGoalRepository(Repository):

    def __init__(self):
        self._registry = list()

    def add(self, entity: Goal) -> None:
        self._registry.append(entity)

    def get(self, id_: str) -> Goal:
        for goal in self._registry:
            if goal.id == id_:
                return goal
        raise EntityNotFoundException

    def __len__(self) -> int:
        return len(self._registry)


class SqlAlchemyGoalRepository(Repository):

    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: Goal) -> None:
        self._session.add(entity)

    def get(self, id_: str) -> Goal:
        goal = self._session.query(Goal).get(id_)
        if goal:
            return goal
        raise EntityNotFoundException

    def __len__(self) -> int:
        return self._session.query(Goal).count()
