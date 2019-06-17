from dependency_injector import containers, providers

from goal_service.application.instrumentation.goal.development import \
    DevelopmentGoalInstrumentation
from goal_service.application.instrumentation.goal.metrics import \
    InMemoryGoalMetrics
from goal_service.application.instrumentation.logger import ConsoleLogger
from goal_service.application.instrumentation.progression.development import \
    DevelopmentProgressionInstrumentation
from goal_service.application.instrumentation.progression.metrics import \
    InMemoryProgressionMetrics


class Instrumentation(containers.DeclarativeContainer):
    goal = providers.Factory(
        DevelopmentGoalInstrumentation, logger=ConsoleLogger(),
        metrics=InMemoryGoalMetrics())
    progression = providers.Factory(
        DevelopmentProgressionInstrumentation, logger=ConsoleLogger(),
        metrics=InMemoryProgressionMetrics())
