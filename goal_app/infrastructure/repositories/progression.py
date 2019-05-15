from sqlalchemy.orm import Session

from goal_app.domain.model.goal import Progression
from goal_app.domain.port import Repository


class InMemoryProgressionRepository(Repository):

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


class SqlAlchemyProgressionRepository(Repository):

    def __init__(self, session: Session):
        self._session = session

    def add(self, progression: Progression) -> None:
        raise Exception("Unable to add progressions directly in the database.")

    def get(self, id_) -> Progression:
        return self._session.query(Progression).get(id_)

    def __len__(self) -> int:
        return self._session.query(Progression).count()
