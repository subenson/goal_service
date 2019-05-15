from goal_app.domain.message.command import SetGoalCommand, \
    CompleteGoalCommand, DiscardGoalCommand, SetGoalProgressionCommand, \
    DiscardGoalProgressionCommand
from goal_app.domain.model.goal import Goal, Progression


class CommandHandler:
    def __init__(self, repository):
        self.repository = repository


class SetGoalCommandHandler(CommandHandler):
    def __call__(self, command: SetGoalCommand):
        goal = Goal(
            name=command.name,
            description=command.description,
            due_date=command.due_date)
        self.repository.add(goal)


class CompleteGoalCommandHandler(CommandHandler):
    def __call__(self, command: CompleteGoalCommand):
        goal = self.repository.get(command.id)
        goal.complete()


class DiscardGoalCommandHandler(CommandHandler):
    def __call__(self, command: DiscardGoalCommand):
        goal = self.repository.get(command.id)
        goal.discard()


class SetGoalProgressionCommandHandler(CommandHandler):
    def __call__(self, command: SetGoalProgressionCommand):
        goal = self.repository.get(command.goal_id)
        goal.add_progression(Progression(
            note=command.note,
            percentage=command.percentage))


class DiscardGoalProgressionCommandHandler(CommandHandler):
    def __call__(self, command: DiscardGoalProgressionCommand):
        progression = self.repository.get(command.id)
        progression.discard()
