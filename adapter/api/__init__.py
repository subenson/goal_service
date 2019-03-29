from flask import Flask, request, jsonify

from adapter.orm import database
from adapter.orm.goal import SqlAlchemyGoalRepository
from application.handler.command import SetGoalCommandHandler, \
    CompleteGoalCommandHandler, DiscardGoalCommandHandler
from application.handler.query import ListOpenGoalsQuery
from domain.message.command import SetGoalCommand, CompleteGoalCommand, \
    DiscardGoalCommand

app = Flask('goal')


@app.route('/', methods=['GET'])
def home():
    return "Hi", 201


@app.route('/goals', methods=['POST'])
def set_goal():
    command = SetGoalCommand(**request.get_json())

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = SetGoalCommandHandler(repository=repository)
        handler(command)

    return "", 204


@app.route('/goals/<id_>/complete', methods=['PUT'])
def complete_goal(id_):
    command = CompleteGoalCommand(id=id_)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = CompleteGoalCommandHandler(repository=repository)
        handler(command)

    return "", 204


@app.route('/goals/<id_>', methods=['DELETE'])
def discard_goal(id_):
    command = DiscardGoalCommand(id=id_)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = DiscardGoalCommandHandler(repository=repository)
        handler(command)

    return "", 204


@app.route('/goals', methods=['GET'])
def list_goals():
    session = database.session()
    list_open_goals = ListOpenGoalsQuery(session)

    return jsonify(list_open_goals())
