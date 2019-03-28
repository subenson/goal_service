from domain.model.goal import Goal


class SetGoalCommandHandler:

    def __init__(self, repository):
        self.repository = repository

    def __call__(self, command):
        goal = Goal(
            name=command.name,
            description=command.description,
            due_date=command.due_date)
        self.repository.add(goal)
