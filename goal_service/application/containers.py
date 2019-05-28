from dependency_injector import providers, containers

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
from goal_service.infrastructure.orm import database


class Core(containers.DeclarativeContainer):
    session = database.session()


class Queries(containers.DeclarativeContainer):
    list_open_goals = providers.Factory(
        ListOpenGoalsQuery, session=Core.session)
    list_progressions = providers.Factory(
        ListProgressionsQuery, session=Core.session)


class Instrumentation(containers.DeclarativeContainer):
    goal = providers.Factory(
        DevelopmentGoalInstrumentation, logger=ConsoleLogger(),
        metrics=InMemoryGoalMetrics())
    progression = providers.Factory(
        DevelopmentProgressionInstrumentation, logger=ConsoleLogger(),
        metrics=InMemoryProgressionMetrics())
