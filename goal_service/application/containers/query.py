from dependency_injector import containers, providers

from goal_service.application.containers.database import Database
from goal_service.application.handlers.query import ListOpenGoalsQuery, \
    ListProgressionsQuery


class Queries(containers.DeclarativeContainer):
    list_open_goals = providers.Factory(
        ListOpenGoalsQuery, session=Database.default.session())
    list_progressions = providers.Factory(
        ListProgressionsQuery, session=Database.default.session())
