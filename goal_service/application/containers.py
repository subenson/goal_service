from dependency_injector import providers, containers

from goal_service.application.handlers.query import ListOpenGoalsQuery, \
    ListProgressionsQuery
from goal_service.application.instrumentation.goal.instrumentation import \
    DevGoalInstrumentation
from goal_service.application.instrumentation.goal.metrics import \
    InMemoryGoalMetrics
from goal_service.application.instrumentation.logger import ConsoleLogger
from goal_service.infrastructure.orm import database


class Core(containers.DeclarativeContainer):
    session = database.session()


class Queries(containers.DeclarativeContainer):
    list_open_goals = providers.Factory(
        ListOpenGoalsQuery, session=Core.session)
    list_progressions = providers.Factory(
        ListProgressionsQuery, session=Core.session)


class Instrumentations(containers.DeclarativeContainer):
    goal = providers.Factory(
        DevGoalInstrumentation, logger=ConsoleLogger(),
        metrics=InMemoryGoalMetrics())
