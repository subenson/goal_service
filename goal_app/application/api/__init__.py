from flask import Flask, request, jsonify

from goal_app.infrastructure.repositories.goal import SqlAlchemyGoalRepository
from goal_app.infrastructure.orm import database
from goal_app.application.handler.command import SetGoalCommandHandler, \
    CompleteGoalCommandHandler, DiscardGoalCommandHandler, \
    SetProgressionCommandHandler
from goal_app.application.handler.query import ListOpenGoalsQuery, \
    ListProgressionsQuery
from goal_app.domain.message.command import SetGoalCommand, \
    CompleteGoalCommand, DiscardGoalCommand, SetProgressionCommand
from goal_app.domain.model import DiscardedEntityException

app = Flask('goal')


def http_ok(body={}, headers=None):
    return jsonify(body), 200, headers


def http_no_content(headers=None):
    return "", 204, headers


def http_conflict(body={}, headers=None):
    return jsonify(body), 409, headers


@app.route('/', methods=['GET'])
def home():
    return http_ok("Hi")


@app.route('/goals', methods=['POST'])
def set_goal():
    command = SetGoalCommand(**request.get_json())

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = SetGoalCommandHandler(repository=repository)
        handler(command)

    return http_no_content()


@app.route('/goals/<id_>/complete', methods=['PUT'])
def complete_goal(id_):
    command = CompleteGoalCommand(id=id_)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = CompleteGoalCommandHandler(repository=repository)

        try:
            handler(command)
            return http_no_content()
        except DiscardedEntityException as ex:
            return http_conflict(dict(reason=str(ex)))


@app.route('/goals/<id_>', methods=['DELETE'])
def discard_goal(id_):
    command = DiscardGoalCommand(id=id_)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = DiscardGoalCommandHandler(repository=repository)

        try:
            handler(command)
            return http_no_content()
        except DiscardedEntityException as ex:
            return http_conflict(dict(reason=str(ex)))


@app.route('/goals', methods=['GET'])
def list_goals():
    open_goals = ListOpenGoalsQuery(database.session())
    return http_ok(open_goals())


@app.route('/goals/<goal_id>/progressions', methods=['GET'])
def list_goal_progressions(goal_id):
    goal_progressions = ListProgressionsQuery(database.session())
    return http_ok(goal_progressions())


@app.route('/goals/<goal_id>/progressions', methods=['POST'])
def set_goal_progression(goal_id):
    progression_json = request.get_json()
    progression_json['goal_id'] = goal_id

    command = SetProgressionCommand(**progression_json)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = SetProgressionCommandHandler(repository=repository)
        handler(command)

    return http_no_content()
