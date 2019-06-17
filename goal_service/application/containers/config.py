from dependency_injector import containers

from goal_service.infrastructure.config import Config


class Config(containers.DeclarativeContainer):
    common = Config('../../common.yaml')
    environment = Config('../../environment.yaml')
