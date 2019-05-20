import unittest
from datetime import datetime

from goal_app.application.handlers.command import AddProgressionCommandHandler, \
    DiscardProgressionCommandHandler, EditProgressionCommandHandler
from goal_app.application.instrumentation.goal import FakeGoalInstrumentation
from goal_app.domain.messages.command import AddProgressionCommand, \
    DiscardProgressionCommand, EditProgressionCommand
from goal_app.infrastructure.repositories.goal import InMemoryGoalRepository
from goal_app.infrastructure.repositories.progression import \
    InMemoryProgressionRepository
from goal_app.domain.models.goal import Goal
from goal_app.domain.models.progression import Progression


class TestGoal(unittest.TestCase):

    A_GOAL_ID = "12345678-1234-5678-9012-123456789012"
    A_GOAL_NAME = "Read a book this week"
    A_GOAL_DESCRIPTION = "7 Habits of Highly Effective People"
    A_GOAL_DUE_DATE = datetime.now()

    A_GOAL_JSON = {
        "name": A_GOAL_NAME,
        "description": A_GOAL_DESCRIPTION,
        "due_date": A_GOAL_DUE_DATE
    }

    A_PROGRESSION_ID = "56789012-1234-5678-9012-123456789012"
    A_PROGRESSION_NOTE = "I read 60 of the 100 pages. It really is a " \
                         "fantastic book!"
    A_PROGRESSION_PERCENTAGE = 60

    A_PROGRESSION_JSON = {
        "note": A_PROGRESSION_NOTE,
        "percentage": A_PROGRESSION_PERCENTAGE
    }

    A_NEW_PROGRESSION_NOTE = "I read 70 of the 100 pages. It really is a " \
                             "fantastic book!"
    A_NEW_PROGRESSION_PERCENTAGE = 70

    def setUp(self):
        self.repository = InMemoryGoalRepository()
        self.repository.add(Goal(**self.A_GOAL_JSON))

    def test_add_progression_should_add_new_progression_to_the_goal(self):
        A_GOAL = self.repository._registry[0]

        # Given
        command = AddProgressionCommand(
            goal_id=A_GOAL.id,
            note=self.A_PROGRESSION_NOTE,
            percentage=self.A_PROGRESSION_PERCENTAGE)

        # When
        handler = AddProgressionCommandHandler(
            repository=self.repository,
            instrumentation=FakeGoalInstrumentation)
        handler(command)

        # Then
        # Get a fresh instance from the repository
        goal = self.repository.get(id_=A_GOAL.id)

        assert len(goal.progressions) == 1
        assert goal.progressions[0].note == self.A_PROGRESSION_NOTE
        assert goal.progressions[0].percentage == self.A_PROGRESSION_PERCENTAGE

    def test_discard_progression_should_flag_goal_as_discarded(self):
        progression = Progression(**self.A_PROGRESSION_JSON)
        progression._id = self.A_PROGRESSION_ID
        progression._goal_id = self.A_GOAL_ID

        repository = InMemoryProgressionRepository()
        repository._registry.append(progression)

        # Given
        command = DiscardProgressionCommand(id=self.A_PROGRESSION_ID)

        # When
        handler = DiscardProgressionCommandHandler(
            repository=repository, instrumentation=FakeGoalInstrumentation)
        handler(command)

        # Then
        assert progression.discarded

    def test_edit_progression(self):
        progression = Progression(**self.A_PROGRESSION_JSON)
        progression._id = self.A_PROGRESSION_ID
        progression._goal_id = self.A_GOAL_ID

        repository = InMemoryProgressionRepository()
        repository._registry.append(progression)

        # Given
        command = EditProgressionCommand(
            id=self.A_PROGRESSION_ID,
            note=self.A_NEW_PROGRESSION_NOTE,
            percentage=self.A_NEW_PROGRESSION_PERCENTAGE)

        # When
        handler = EditProgressionCommandHandler(
            repository=repository, instrumentation=FakeGoalInstrumentation)
        handler(command)

        # Then
        assert progression.note == self.A_NEW_PROGRESSION_NOTE
        assert progression.percentage == self.A_NEW_PROGRESSION_PERCENTAGE
