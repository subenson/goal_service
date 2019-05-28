from goal_service.domain.models.goal import create_goal
from goal_service.infrastructure.orm.database import database
from goal_service.application.handlers.command import SetGoalCommandHandler
from goal_service.domain.messages.command import SetGoalCommand
from goal_service.infrastructure.repositories.goal import \
    SqlAlchemyGoalRepository
from goal_service.application.containers import Instrumentation


if __name__ == '__main__':

    print('Running Main')

    command = SetGoalCommand(
        name="First Goal!",
        description="2019 will be my best year!",
        due_date=None)

    with database.unit_of_work() as session:
        repository = SqlAlchemyGoalRepository(session)
        handler = SetGoalCommandHandler(
            factory=create_goal,
            repository=repository,
            instrumentation=Instrumentation.goal()
        )

        print(f'Count goals: {len(repository)}')
        print(f'Handle Command: {command.name}')
        handler(command)

        print(f'Count goals: {len(repository)}')
