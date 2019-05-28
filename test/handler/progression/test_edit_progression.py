import unittest
from datetime import datetime

from mockito import mock, when, verify

from goal_service.application.handlers.command import \
    EditProgressionCommandHandler
from goal_service.application.instrumentation.goal.instrumentation import \
    GoalInstrumentation
from goal_service.domain.messages.command import EditProgressionCommand
from goal_service.domain.models.goal import Goal
from goal_service.domain.models.progression import Progression, \
    create_progression
from goal_service.domain.port import Repository
from goal_service.infrastructure.repositories import EntityNotFoundException


class TestProgressionCommandHandler(unittest.TestCase):

    A_GOAL_ID = "12345678-1234-5678-9012-123456789012"
    A_GOAL_NAME = "Name"
    A_GOAL_DESCRIPTION = "Description"
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
    A_PROGRESSION_NOTE = "Note"
    A_PROGRESSION_PERCENTAGE = 5
    A_PROGRESSION_JSON = {
        "note": A_PROGRESSION_NOTE,
        "percentage": A_PROGRESSION_PERCENTAGE
    }
    A_PROGRESSION = mock({
        "id": A_PROGRESSION_ID,
        "note": A_PROGRESSION_NOTE,
        "percentage": A_PROGRESSION_PERCENTAGE
    }, spec=Progression)

    A_NEW_NOTE = "New note"
    A_NEW_PERCENTAGE = 10

    def setUp(self):
        self.factory = mock(create_progression)
        self.repository = mock(Repository)
        self.instrument = mock(GoalInstrumentation)

        when(self.instrument).edit_progression(
            self.A_PROGRESSION).thenReturn(None)
        when(self.instrument).progression_lookup_failed(
            self.A_PROGRESSION_ID).thenReturn(None)

    def test_edit_progression(self):
        # Given
        command = EditProgressionCommand(
            id=self.A_PROGRESSION_ID,
            note=self.A_NEW_NOTE,
            percentage=self.A_NEW_PERCENTAGE)

        when(self.repository).get(self.A_PROGRESSION_ID).thenReturn(
            self.A_PROGRESSION)

        # When
        handler = EditProgressionCommandHandler(
            repository=self.repository, instrumentation=self.instrument)
        handler(command)

        # Then
        assert self.A_PROGRESSION.note == self.A_NEW_NOTE
        assert self.A_PROGRESSION.percentage == self.A_NEW_PERCENTAGE
        verify(self.instrument, times=1).edit_progression(self.A_PROGRESSION)

    def test_edit_progression_lookup_failed(self):
        # Given
        command = EditProgressionCommand(
            id=self.A_PROGRESSION_ID,
            note=self.A_NEW_NOTE,
            percentage=self.A_NEW_PERCENTAGE)

        when(self.repository).get(self.A_PROGRESSION_ID).thenRaise(
            EntityNotFoundException)

        # When
        with self.assertRaises(EntityNotFoundException):
            handler = EditProgressionCommandHandler(
                repository=self.repository, instrumentation=self.instrument)
            handler(command)

        # Then
        verify(self.instrument, times=1).progression_lookup_failed(
            self.A_PROGRESSION_ID)
