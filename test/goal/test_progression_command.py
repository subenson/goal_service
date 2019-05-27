import unittest
from datetime import datetime

from mockito import mock, when, verify

from goal_service.application.handlers.command import \
    AddProgressionCommandHandler, DiscardProgressionCommandHandler, \
    EditProgressionCommandHandler
from goal_service.application.instrumentation.goal.instrumentation import \
    GoalInstrumentation
from goal_service.domain.messages.command import AddProgressionCommand, \
    DiscardProgressionCommand, EditProgressionCommand
from goal_service.domain.models.goal import Goal
from goal_service.domain.models.progression import Progression, \
    create_progression
from goal_service.infrastructure.repositories.goal import \
    InMemoryGoalRepository


class TestProgressionCommandHandler(unittest.TestCase):

    A_GOAL_ID = "12345678-1234-5678-9012-123456789012"
    A_GOAL_NAME = "Read a book this week"
    A_GOAL_DESCRIPTION = "7 Habits of Highly Effective People"
    A_GOAL_DUE_DATE = datetime.now()

    A_GOAL_JSON = {
        "name": A_GOAL_NAME,
        "description": A_GOAL_DESCRIPTION,
        "due_date": A_GOAL_DUE_DATE
    }

    A_GOAL = mock({
        "id": A_GOAL_ID,
        "name": A_GOAL_NAME,
        "description": A_GOAL_DESCRIPTION,
        "due_date": A_GOAL_DUE_DATE
    }, spec=Goal)

    A_PROGRESSION_ID = "56789012-1234-5678-9012-123456789012"
    A_PROGRESSION_NOTE = "I read 60 of the 100 pages. It really is a " \
                         "fantastic book!"
    A_PROGRESSION_PERCENTAGE = 60

    A_PROGRESSION_JSON = {
        "note": A_PROGRESSION_NOTE,
        "percentage": A_PROGRESSION_PERCENTAGE
    }

    A_PROGRESSION = mock({
        "id": A_PROGRESSION_ID,
        "note": A_PROGRESSION_NOTE,
        "percentage": A_PROGRESSION_PERCENTAGE
    }, spec=Progression)

    A_NEW_PROGRESSION_NOTE = "I read 70 of the 100 pages. It really is a " \
                             "fantastic book!"
    A_NEW_PROGRESSION_PERCENTAGE = 70

    def setUp(self):
        self.factory = mock(create_progression)
        self.repository = InMemoryGoalRepository()
        self.instrumentation = mock(GoalInstrumentation)

    def test_add_progression_should_add_new_progression_to_the_goal(self):
        when(self.repository).get(self.A_GOAL_ID).thenReturn(
            self.A_GOAL)
        when(self.factory).__call__(**self.A_PROGRESSION_JSON).thenReturn(
            self.A_PROGRESSION)
        when(self.instrumentation).add_progression(
            self.A_GOAL).thenReturn(None)
        when(self.A_GOAL).add_progression(self.A_PROGRESSION).thenReturn(None)

        # Given
        command = AddProgressionCommand(
            goal_id=self.A_GOAL_ID,
            note=self.A_PROGRESSION_NOTE,
            percentage=self.A_PROGRESSION_PERCENTAGE)

        # When
        handler = AddProgressionCommandHandler(
            factory=self.factory,
            repository=self.repository,
            instrumentation=self.instrumentation)
        handler(command)

        # Then
        verify(self.A_GOAL, times=1).add_progression(self.A_PROGRESSION)

    def test_discard_progression_should_flag_goal_as_discarded(self):
        when(self.instrumentation).discard_progression(
            self.A_PROGRESSION).thenReturn(None)
        when(self.A_PROGRESSION).discard().thenReturn(None)

        self.repository.add(self.A_PROGRESSION)

        # Given
        command = DiscardProgressionCommand(id=self.A_PROGRESSION_ID)

        # When
        handler = DiscardProgressionCommandHandler(
            repository=self.repository, instrumentation=self.instrumentation)
        handler(command)

        # Then
        verify(self.A_PROGRESSION, times=1).discard()

    def test_edit_progression(self):
        when(self.instrumentation).edit_progression(
            self.A_PROGRESSION).thenReturn(None)

        self.repository.add(self.A_PROGRESSION)

        # Given
        command = EditProgressionCommand(
            id=self.A_PROGRESSION_ID,
            note=self.A_NEW_PROGRESSION_NOTE,
            percentage=self.A_NEW_PROGRESSION_PERCENTAGE)

        # When
        handler = EditProgressionCommandHandler(
            repository=self.repository, instrumentation=self.instrumentation)
        handler(command)

        # Then
        assert self.A_PROGRESSION.note == self.A_NEW_PROGRESSION_NOTE
        assert self.A_PROGRESSION.percentage == \
               self.A_NEW_PROGRESSION_PERCENTAGE
