from flask import Flask, request

from adapter.orm.goal import SqlAlchemyGoalRepository
from application.handler.command import SetGoalCommandHandler
from domain.message.command import SetGoalCommand
from adapter.config import database

app = Flask('goal')


@app.route('/', methods=['GET'])
def home():
    return "Hi", 201


@app.route('/goals', methods=['POST'])
def set_goal():
    command = SetGoalCommand(**request.get_json())

    session = database.get_session()
    repository = SqlAlchemyGoalRepository(session)
    handler = SetGoalCommandHandler(repository=repository)

    handler(command)

    return "", 204
