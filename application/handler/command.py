from domain.message.command import SetGoalCommand, CompleteGoalCommand
from domain.model.goal import Goal


class SetGoalCommandHandler:

    def __init__(self, repository):
        self.repository = repository

    def __call__(self, command: SetGoalCommand):
        goal = Goal(
            name=command.name,
            description=command.description,
            due_date=command.due_date)
        self.repository.add(goal)


class CompleteGoalHandler:

    def __init__(self, repository):
        self.repository = repository

    def __call__(self, command: CompleteGoalCommand):
        goal = self.repository.get(command.id)
        goal.complete()
        self.repository._session.commit()  # Fix this ASAP.
