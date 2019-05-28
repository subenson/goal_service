import unittest
from datetime import datetime

from mockito import mock, when, verify

from goal_service.application.handlers import RelatedEntityNotFoundException
from goal_service.application.handlers.command import \
    CompleteGoalCommandHandler
from goal_service.application.instrumentation.goal.instrumentation import \
    GoalInstrumentation
from goal_service.domain.messages.command import CompleteGoalCommand
from goal_service.domain.models import DiscardedEntityException
from goal_service.domain.models.goal import Goal
from goal_service.domain.port import Repository
from goal_service.infrastructure.repositories import EntityNotFoundException


class TestGoalCommandHandler(unittest.TestCase):

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
    A_DISCARDED_GOAL = mock({
        "id": A_GOAL_ID,
        "discarded": True
    }, spec=Goal)

    def setUp(self):
        self.repository = mock(Repository)
        self.instrument = mock(GoalInstrumentation)

        when(self.A_GOAL).complete().thenReturn(None)

    def test_complete_goal(self):
        # Given
        command = CompleteGoalCommand(id=self.A_GOAL_ID)

        when(self.repository).get(self.A_GOAL_ID).thenReturn(self.A_GOAL)
        when(self.instrument).goal_completed(self.A_GOAL).thenReturn(None)

        # When
        handler = CompleteGoalCommandHandler(
            repository=self.repository,
            instrumentation=self.instrument)
        handler(command)

        # Then
        verify(self.A_GOAL, times=1).complete()
        verify(self.instrument, times=1).goal_completed(self.A_GOAL)

    def test_complete_discarded_goal(self):

        # Given
        command = CompleteGoalCommand(id=self.A_GOAL_ID)

        when(self.repository).get(self.A_GOAL_ID).thenReturn(
            self.A_DISCARDED_GOAL)
        when(self.A_DISCARDED_GOAL).complete().thenRaise(
            DiscardedEntityException)

        # When
        with self.assertRaises(DiscardedEntityException):
            handler = CompleteGoalCommandHandler(
                repository=self.repository,
                instrumentation=self.instrument)
            handler(command)

    def test_complete_goal_lookup_failed(self):
        # Given
        command = CompleteGoalCommand(id=self.A_GOAL_ID)

        when(self.repository).get(self.A_GOAL_ID).thenRaise(
            EntityNotFoundException)
        when(self.instrument).goal_lookup_failed(self.A_GOAL_ID).thenReturn(
            None)

        # When
        with self.assertRaises(RelatedEntityNotFoundException):
            handler = CompleteGoalCommandHandler(
                repository=self.repository,
                instrumentation=self.instrument)
            handler(command)

        verify(self.instrument, times=1).goal_lookup_failed(
            self.A_GOAL_ID)
