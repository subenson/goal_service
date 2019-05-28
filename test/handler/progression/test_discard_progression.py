import unittest
from datetime import datetime

from mockito import mock, when, verify

from goal_service.application.handlers.command import \
    DiscardProgressionCommandHandler
from goal_service.application.instrumentation.goal.instrumentation import \
    GoalInstrumentation
from goal_service.domain.messages.command import DiscardProgressionCommand
from goal_service.domain.models.goal import Goal
from goal_service.domain.models.progression import Progression, \
    create_progression
from goal_service.domain.port import Repository
from goal_service.infrastructure.repositories import EntityNotFoundException


class TestDiscardProgression(unittest.TestCase):

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

    def setUp(self):
        self.factory = mock(create_progression)
        self.repository = mock(Repository)
        self.instrument = mock(GoalInstrumentation)

        when(self.instrument).discard_progression(
            self.A_PROGRESSION).thenReturn(None)
        when(self.A_PROGRESSION).discard().thenReturn(None)
        when(self.instrument).progression_lookup_failed(...).thenReturn(None)

    def test_discard_progression(self):
        # Given
        command = DiscardProgressionCommand(id=self.A_PROGRESSION_ID)

        when(self.repository).get(self.A_PROGRESSION_ID).thenReturn(
            self.A_PROGRESSION)

        # When
        handler = DiscardProgressionCommandHandler(
            repository=self.repository, instrumentation=self.instrument)
        handler(command)

        # Then
        verify(self.A_PROGRESSION, times=1).discard()
        verify(self.instrument, times=1).discard_progression(
            self.A_PROGRESSION)

    def test_discard_progression_goal_lookup_failed_instrumentation(self):
        # Given
        command = DiscardProgressionCommand(id=self.A_PROGRESSION_ID)

        when(self.repository).get(self.A_PROGRESSION_ID).thenRaise(
            EntityNotFoundException)

        # When
        with self.assertRaises(EntityNotFoundException):
            handler = DiscardProgressionCommandHandler(
                repository=self.repository,
                instrumentation=self.instrument)
            handler(command)

        verify(self.instrument, times=1).progression_lookup_failed(
            self.A_PROGRESSION_ID)
