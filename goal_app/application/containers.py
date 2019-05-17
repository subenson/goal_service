from dependency_injector import providers, containers

from goal_app.application.handlers.query import ListOpenGoalsQuery, \
    ListProgressionsQuery
from goal_app.infrastructure.orm import database


class Core(containers.DeclarativeContainer):
    session = database.session()


class Queries(containers.DeclarativeContainer):
    list_open_goals = providers.Factory(
        ListOpenGoalsQuery, session=Core.session)
    list_progressions = providers.Factory(
        ListProgressionsQuery, session=Core.session)
