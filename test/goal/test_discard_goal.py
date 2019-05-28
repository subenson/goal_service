import unittest
from datetime import datetime

from mockito import mock, when, verify

from goal_service.application.handlers.command import DiscardGoalCommandHandler
from goal_service.application.instrumentation.goal.instrumentation import \
    GoalInstrumentation
from goal_service.domain.messages.command import CompleteGoalCommand, \
    DiscardGoalCommand
from goal_service.domain.models import DiscardedEntityException
from goal_service.domain.models.goal import Goal, create_goal
from goal_service.domain.port import Repository


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
        self.factory = mock(create_goal)
        self.repository = mock(Repository)
        self.instrumentation = mock(GoalInstrumentation)

    def test_discard_goal(self):
        # Given
        command = DiscardGoalCommand(id=self.A_GOAL_ID)

        when(self.repository).get(self.A_GOAL_ID).thenReturn(self.A_GOAL)
        when(self.A_GOAL).discard().thenReturn(None)
        when(self.instrumentation).goal_discarded(self.A_GOAL).thenReturn(None)

        # When
        handler = DiscardGoalCommandHandler(
            repository=self.repository,
            instrumentation=self.instrumentation)
        handler(command)

        # Then
        verify(self.A_GOAL, times=1).discard()
        verify(self.instrumentation, times=1).goal_discarded(self.A_GOAL)

    def test_discard_discarded_goal(self):
        # Given
        command = CompleteGoalCommand(id=self.A_GOAL_ID)

        when(self.repository).get(self.A_GOAL_ID).thenReturn(
            self.A_DISCARDED_GOAL)
        when(self.A_DISCARDED_GOAL).discard().thenRaise(
            DiscardedEntityException)

        # When
        with self.assertRaises(DiscardedEntityException):
            handler = DiscardGoalCommandHandler(
                repository=self.repository,
                instrumentation=self.instrumentation)
            handler(command)
