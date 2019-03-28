from flask import Flask, request, jsonify

from adapter.orm.goal import SqlAlchemyGoalRepository
from application.handler.command import SetGoalCommandHandler, \
    CompleteGoalHandler
from application.handler.query import ListOpenGoalsQuery
from domain.message.command import SetGoalCommand, CompleteGoalCommand
from adapter.config import database

app = Flask('goal')


@app.route('/', methods=['GET'])
def home():
    return "Hi", 201


@app.route('/goals', methods=['POST'])
def set_goal():
    session = database.get_session()
    repository = SqlAlchemyGoalRepository(session)

    command = SetGoalCommand(**request.get_json())
    handler = SetGoalCommandHandler(repository=repository)
    handler(command)

    return "", 204


@app.route('/goals/<id_>/complete', methods=['PUT'])
def complete_goal(id_):
    session = database.get_session()
    repository = SqlAlchemyGoalRepository(session)

    command = CompleteGoalCommand(id=id_)
    handler = CompleteGoalHandler(repository=repository)
    handler(command)

    return "", 204


@app.route('/goals', methods=['GET'])
def list_goals():
    session = database.get_session()

    list_open_goals = ListOpenGoalsQuery(session)
    return jsonify(list_open_goals())
