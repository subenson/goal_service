# pylint: disable=unused-argument
from flask import Flask, request, jsonify

from goal_service.application.containers import Queries, Instrumentations
from goal_service.application.handlers import RelatedEntityNotFoundException
from goal_service.domain.models.goal import create_goal
from goal_service.domain.models.progression import create_progression
from goal_service.domain.models.progression import InvalidPercentageException
from goal_service.infrastructure.repositories import EntityNotFoundException
from goal_service.infrastructure.repositories.goal import \
    SqlAlchemyGoalRepository
from goal_service.infrastructure.orm import database
from goal_service.application.handlers.command import SetGoalCommandHandler, \
    CompleteGoalCommandHandler, DiscardGoalCommandHandler, \
    AddProgressionCommandHandler, DiscardProgressionCommandHandler, \
    EditProgressionCommandHandler, SetSubGoalCommandHandler
from goal_service.domain.messages.command import SetGoalCommand, \
    CompleteGoalCommand, DiscardGoalCommand, AddProgressionCommand, \
    DiscardProgressionCommand, EditProgressionCommand, SetSubGoalCommand
from goal_service.domain.models import DiscardedEntityException
from goal_service.infrastructure.repositories.progression import \
    SqlAlchemyProgressionRepository

app = Flask('goal')


@app.errorhandler(DiscardedEntityException)
def discarded_entity_error(error):
    return http_conflict(dict(reason=error.__str__()))


@app.errorhandler(InvalidPercentageException)
def invalid_percentage_exception(error):
    return http_conflict(dict(reason=error.__str__()))


@app.errorhandler(EntityNotFoundException)
def entity_not_found_exception(error):
    return http_not_found(dict(reason=error.__str__()))


@app.errorhandler(RelatedEntityNotFoundException)
def related_entity_not_found_exception(error):
    return http_bad_request(dict(reason=error.__str__()))


def http_ok(body=None, headers=None):
    return jsonify(body or {}), 200, headers


def http_no_content(headers=None):
    return "", 204, headers


def http_conflict(body=None, headers=None):
    return jsonify(body or {}), 409, headers


def http_not_found(body=None, headers=None):
    return jsonify(body or {}), 404, headers


def http_bad_request(body=None, headers=None):
    return jsonify(body or {}), 400, headers


@app.route('/', methods=['GET'])
def home():
    return http_ok("Hi")


@app.route('/goals', methods=['POST'])
def set_goal():
    command = SetGoalCommand(**request.get_json())

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = SetGoalCommandHandler(  # To-do: IoC
            factory=create_goal,
            repository=repository,
            instrumentation=Instrumentations.goal())
        handler(command)

    return http_no_content()


@app.route('/goals/<id_>/complete', methods=['PUT'])
def complete_goal(id_):
    command = CompleteGoalCommand(id=id_)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = CompleteGoalCommandHandler(
            repository=repository,  # To-do: IoC
            instrumentation=Instrumentations.goal())
        handler(command)
        return http_no_content()


@app.route('/goals/<id_>', methods=['DELETE'])
def discard_goal(id_):
    command = DiscardGoalCommand(id=id_)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = DiscardGoalCommandHandler(
            repository=repository,  # To-do: IoC
            instrumentation=Instrumentations.goal())
        handler(command)
        return http_no_content()


@app.route('/goals', methods=['GET'])
def list_goals():
    open_goals_query = Queries.list_open_goals()
    return http_ok(open_goals_query())


@app.route('/goals/<goal_id>/progressions', methods=['GET'])
def list_goal_progressions(goal_id):
    query = Queries.list_progressions()
    progressions = query(goal_id=goal_id)
    return http_ok(progressions)


@app.route('/goals/<goal_id>/progressions', methods=['POST'])
def add_progression(goal_id):
    progression_json = request.get_json()
    progression_json['goal_id'] = goal_id

    command = AddProgressionCommand(**progression_json)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = AddProgressionCommandHandler(
            factory=create_progression,
            repository=repository,
            instrumentation=Instrumentations.goal())
        handler(command)
        return http_no_content()


@app.route('/goals/<goal_id>/progressions/<progression_id>', methods=[
    'DELETE'])
def discard_progression(goal_id, progression_id):
    command = DiscardProgressionCommand(id=progression_id)

    with database.unit_of_work() as session:
        repository = SqlAlchemyProgressionRepository(session)
        handler = DiscardProgressionCommandHandler(
            repository=repository,  # To-do: IoC
            instrumentation=Instrumentations.goal())
        handler(command)
        return http_no_content()


@app.route('/goals/<goal_id>/progressions/<progression_id>', methods=[
    'PUT'])
def edit_progression(goal_id, progression_id):
    progression_json = request.get_json()
    command = EditProgressionCommand(
        id=progression_id,
        note=progression_json.get('note'),
        percentage=progression_json.get('percentage'))

    with database.unit_of_work() as session:
        repository = SqlAlchemyProgressionRepository(session)
        handler = EditProgressionCommandHandler(
            repository=repository,  # To-do: IoC
            instrumentation=Instrumentations.goal())
        handler(command)
        return http_no_content()


@app.route('/goals/<goal_id>/subgoals', methods=['GET'])
def list_subgoals(goal_id):
    open_goals_query = Queries.list_open_goals()
    return http_ok(open_goals_query(goal_id))


@app.route('/goals/<goal_id>/subgoals', methods=['POST'])
def set_subgoal(goal_id):
    goal_json = request.get_json()
    goal_json['main_goal_id'] = goal_id
    command = SetSubGoalCommand(**goal_json)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = SetSubGoalCommandHandler(  # To-do: IoC
            factory=create_goal,
            repository=repository,
            instrumentation=Instrumentations.goal())
        handler(command)
    return http_no_content()
