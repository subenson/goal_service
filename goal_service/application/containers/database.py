from dependency_injector import containers

from goal_service.application.containers.config import Config
from goal_service.infrastructure.orm.database import SqlAlchemy


class Database(containers.DeclarativeContainer):
    default = SqlAlchemy(
        driver=Config.environment.get('orm', 'driver'),
        user=Config.environment.get('orm', 'user'),
        password=Config.environment.get('orm', 'password'),
        host=Config.environment.get('orm', 'host'),
        port=Config.environment.get('orm', 'port'),
        database=Config.environment.get('orm', 'database'))
