import unittest
from datetime import datetime

from mockito import mock, when, verify

from goal_service.application.handlers import RelatedEntityNotFoundException
from goal_service.application.handlers.command import SetGoalCommandHandler, \
    CompleteGoalCommandHandler, DiscardGoalCommandHandler
from goal_service.application.instrumentation.goal.instrumentation import \
    GoalInstrumentation
from goal_service.domain.messages.command import SetGoalCommand, \
    CompleteGoalCommand, DiscardGoalCommand
from goal_service.domain.models.goal import Goal, create_goal
from goal_service.domain.port import Repository
from goal_service.infrastructure.repositories import EntityNotFoundException


class TestGoalInstrumentation(unittest.TestCase):

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

    def setUp(self):
        self.factory = mock(create_goal)
        self.repository = mock(Repository)
        self.instrumentation = mock(GoalInstrumentation)

        when(self.factory).__call__(**self.A_GOAL_JSON).thenReturn(self.A_GOAL)
        when(self.repository).add(self.A_GOAL).thenReturn(None)
        when(self.instrumentation).goal_set(self.A_GOAL).thenReturn(None)
        when(self.instrumentation).goal_lookup_failed(...).thenReturn(None)

    def test_goal_set_instrumentation(self):
        # Given
        command = SetGoalCommand(
            name=self.A_GOAL_NAME,
            description=self.A_GOAL_DESCRIPTION,
            due_date=self.A_GOAL_DUE_DATE)

        # When
        handler = SetGoalCommandHandler(
            factory=self.factory,
            repository=self.repository,
            instrumentation=self.instrumentation)
        handler(command)

        # Then
        verify(self.instrumentation, times=1).goal_set(self.A_GOAL)

    def test_complete_goal_lookup_failed_instrumentation(self):
        # Given
        command = CompleteGoalCommand(id=self.A_GOAL_ID)

        when(self.repository).get(self.A_GOAL_ID).thenRaise(
            EntityNotFoundException)

        # When
        with self.assertRaises(RelatedEntityNotFoundException):
            handler = CompleteGoalCommandHandler(
                repository=self.repository,
                instrumentation=self.instrumentation)
            handler(command)

        verify(self.instrumentation, times=1).goal_lookup_failed(
            self.A_GOAL_ID)

    def test_discard_goal_lookup_failed_instrumentation(self):
        # Given
        command = DiscardGoalCommand(id=self.A_GOAL_ID)

        when(self.repository).get(self.A_GOAL_ID).thenRaise(
            EntityNotFoundException)

        # When
        with self.assertRaises(RelatedEntityNotFoundException):
            handler = DiscardGoalCommandHandler(
                repository=self.repository,
                instrumentation=self.instrumentation)
            handler(command)

        verify(self.instrumentation, times=1).goal_lookup_failed(
            self.A_GOAL_ID)
