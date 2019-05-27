from sqlalchemy.orm import Session

from goal_service.domain.models.progression import Progression
from goal_service.domain.port import Repository
from goal_service.infrastructure.repositories import EntityNotFoundException


class InMemoryProgressionRepository(Repository):

    def __init__(self):
        self._registry = list()

    def add(self, progression: Progression) -> None:
        raise Exception("Unable to add progressions directly in the database.")

    def get(self, id_) -> Progression:
        for progression in self._registry:
            if progression.id == id_:
                return progression
        return EntityNotFoundException

    def __len__(self) -> int:
        return len(self._registry)


class SqlAlchemyProgressionRepository(Repository):

    def __init__(self, session: Session):
        self._session = session

    def add(self, progression: Progression) -> None:
        raise Exception("Unable to add progressions directly in the database.")

    def get(self, id_) -> Progression:
        progression = self._session.query(Progression).get(id_)
        if progression:
            return progression
        raise EntityNotFoundException

    def __len__(self) -> int:
        return self._session.query(Progression).count()
