from datetime import datetime

from application.handler.command import SetGoalCommandHandler
from domain.message.command import SetGoalCommand
from adapter.orm.goal import SqlAlchemyGoalRepository
from adapter.orm import SqlAlchemy


db = SqlAlchemy('sqlite:///test.db')
db.configure_mappings()
db.create_schema()


if __name__ == '__main__':

    print('Running Main')

    session = db.get_session()
    registry = SqlAlchemyGoalRepository(session)

    handler = SetGoalCommandHandler(registry=registry)

    command = SetGoalCommand(
        name="First Goal!",
        description="2019 will be my best year!",
        due_date=datetime.now())

    print(f'Count goals: {len(registry)}')
    print(f'Handle Command: {command.name}')
    handler(command)

    print(f'Count goals: {len(registry)}')
