from abc import ABCMeta, abstractmethod

from goal_service.domain.models import Entity


class Repository(metaclass=ABCMeta):

    @abstractmethod
    def add(self, entity: Entity) -> None:
        pass

    @abstractmethod
    def get(self, id_: str) -> Entity:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass
