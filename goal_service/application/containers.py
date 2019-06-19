from dependency_injector import containers, providers

from goal_service.application.handlers.query import ListOpenGoalsQuery, \
    ListProgressionsQuery
from goal_service.application.instrumentation.goal.development import \
    DevelopmentGoalInstrumentation
from goal_service.application.instrumentation.goal.metrics import \
    InMemoryGoalMetrics
from goal_service.application.instrumentation.logger import ConsoleLogger
from goal_service.application.instrumentation.progression.development import \
    DevelopmentProgressionInstrumentation
from goal_service.application.instrumentation.progression.metrics import \
    InMemoryProgressionMetrics
from goal_service.infrastructure.config import Config
from goal_service.infrastructure.orm.database import SqlAlchemy
from goal_service.infrastructure.orm.mapping import DatabaseMapping
from goal_service.infrastructure.orm.schema import DatabaseSchema


class Core(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    config.override(Config(['common.yaml', 'environment.yaml']).read())


class Gateway(containers.DeclarativeContainer):
    database = SqlAlchemy(
        driver=Core.config.orm.driver(),
        user=Core.config.orm.user(),
        password=Core.config.orm.password(),
        host=Core.config.orm.host(),
        port=Core.config.orm.port(),
        database=Core.config.orm.database())
    database_schema = DatabaseSchema(database)
    database_mapping = DatabaseMapping(schema=database_schema)


class Instrumentation(containers.DeclarativeContainer):
    goal = providers.Factory(
        DevelopmentGoalInstrumentation, logger=ConsoleLogger(),
        metrics=InMemoryGoalMetrics())
    progression = providers.Factory(
        DevelopmentProgressionInstrumentation, logger=ConsoleLogger(),
        metrics=InMemoryProgressionMetrics())


class Queries(containers.DeclarativeContainer):
    list_open_goals = providers.Factory(
        ListOpenGoalsQuery, session=Gateway.database.session())
    list_progressions = providers.Factory(
        ListProgressionsQuery, session=Gateway.database.session())
