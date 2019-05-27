from goal_service.infrastructure.orm.database import database
from goal_service.application.handlers.command import SetGoalCommandHandler
from goal_service.domain.messages.command import SetGoalCommand
from goal_service.infrastructure.repositories.goal import \
    SqlAlchemyGoalRepository


if __name__ == '__main__':

    print('Running Main')

    command = SetGoalCommand(
        name="First Goal!",
        description="2019 will be my best year!",
        due_date=None)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = SetGoalCommandHandler(repository=repository)

        print(f'Count goals: {len(repository)}')
        print(f'Handle Command: {command.name}')
        handler(command)

        print(f'Count goals: {len(repository)}')
