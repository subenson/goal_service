import unittest

from mockito import mock, when, verify

from goal_service.application.handlers import RelatedEntityNotFoundException
from goal_service.application.handlers.command import \
    AddProgressionCommandHandler
from goal_service.application.instrumentation.goal.instrumentation import \
    GoalInstrumentation
from goal_service.domain.messages.command import AddProgressionCommand
from goal_service.domain.models.goal import Goal
from goal_service.domain.models.progression import create_progression, \
    Progression
from goal_service.domain.port import Repository
from goal_service.infrastructure.repositories import EntityNotFoundException


class TestAddProgression(unittest.TestCase):

    A_GOAL_ID = "12345678-1234-5678-9012-123456789012"
    A_GOAL = mock({
        "id": A_GOAL_ID
    }, spec=Goal)

    A_PROGRESSION_ID = "22345678-1234-5678-9012-123456789012"
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

        when(self.factory).__call__(**self.A_PROGRESSION_JSON).thenReturn(
            self.A_PROGRESSION)
        when(self.A_GOAL).add_progression(self.A_PROGRESSION).thenReturn(None)
        when(self.instrument).add_progression(self.A_GOAL).thenReturn(None)
        when(self.instrument).goal_lookup_failed(...).thenReturn(None)

    def test_add_progression(self):
        when(self.repository).get(self.A_GOAL_ID).thenReturn(self.A_GOAL)

        # Given
        command = AddProgressionCommand(
            goal_id=self.A_GOAL_ID,
            note=self.A_PROGRESSION_NOTE,
            percentage=self.A_PROGRESSION_PERCENTAGE)

        # When
        handler = AddProgressionCommandHandler(
            factory=self.factory,
            repository=self.repository,
            instrumentation=self.instrument)
        handler(command)

        # Then
        verify(self.A_GOAL, times=1).add_progression(self.A_PROGRESSION)
        verify(self.factory, times=1).__call__(**self.A_PROGRESSION_JSON)

    def test_add_progression_instrumentation(self):
        # Given
        command = AddProgressionCommand(
            goal_id=self.A_GOAL_ID,
            note=self.A_PROGRESSION_NOTE,
            percentage=self.A_PROGRESSION_PERCENTAGE)

        when(self.repository).get(self.A_GOAL_ID).thenReturn(self.A_GOAL)

        # When
        handler = AddProgressionCommandHandler(
            factory=self.factory,
            repository=self.repository,
            instrumentation=self.instrument)
        handler(command)

        # Then
        verify(self.instrument, times=1).add_progression(self.A_GOAL)

    def test_add_progression_goal_lookup_failed_instrumentation(self):
        # Given
        command = AddProgressionCommand(
            goal_id=self.A_GOAL_ID,
            note=self.A_PROGRESSION_NOTE,
            percentage=self.A_PROGRESSION_PERCENTAGE)

        when(self.repository).get(self.A_GOAL_ID).thenRaise(
            EntityNotFoundException)

        # When
        with self.assertRaises(RelatedEntityNotFoundException):
            handler = AddProgressionCommandHandler(
                factory=self.factory,
                repository=self.repository,
                instrumentation=self.instrument)
            handler(command)

        verify(self.instrument, times=1).goal_lookup_failed(
            self.A_GOAL_ID, ...)
