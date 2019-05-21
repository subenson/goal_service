from goal_app.domain.messages.command import SetGoalCommand, \
    CompleteGoalCommand, DiscardGoalCommand, AddProgressionCommand, \
    DiscardProgressionCommand, EditProgressionCommand
from goal_app.domain.models.goal import Goal
from goal_app.domain.models.progression import Progression


class CommandHandler:
    def __init__(self, repository, instrumentation):
        self.repository = repository
        self.instrumentation = instrumentation


class FactoryCommandHandler:
    def __init__(self, factory, repository, instrumentation):
        self.factory = factory
        self.repository = repository
        self.instrumentation = instrumentation


class SetGoalCommandHandler(FactoryCommandHandler):
    def __call__(self, command: SetGoalCommand):
        goal = self.factory(
            name=command.name,
            description=command.description,
            due_date=command.due_date)
        self.repository.add(goal)
        self.instrumentation.goal_set(goal)


class CompleteGoalCommandHandler(CommandHandler):
    def __call__(self, command: CompleteGoalCommand):
        goal = self.repository.get(command.id)
        goal.complete()
        self.instrumentation.goal_completed(goal)


class DiscardGoalCommandHandler(CommandHandler):
    def __call__(self, command: DiscardGoalCommand):
        goal = self.repository.get(command.id)
        goal.discard()
        self.instrumentation.goal_discarded(goal)


class AddProgressionCommandHandler(CommandHandler):
    def __call__(self, command: AddProgressionCommand):
        goal = self.repository.get(command.goal_id)
        goal.add_progression(Progression(
            note=command.note,
            percentage=command.percentage))
        self.instrumentation.add_progression(goal)


class DiscardProgressionCommandHandler(CommandHandler):
    def __call__(self, command: DiscardProgressionCommand):
        progression = self.repository.get(command.id)
        progression.discard()
        self.instrumentation.discard_progression(progression)


class EditProgressionCommandHandler(CommandHandler):
    def __call__(self, command: EditProgressionCommand):
        progression = self.repository.get(command.id)
        progression.note = command.note
        progression.percentage = command.percentage
        self.instrumentation.edit_progression(progression)
