import unittest
from datetime import datetime

from mockito import mock, when, verify

from goal_service.application.handlers.command import SetGoalCommandHandler
from goal_service.application.instrumentation.goal.interface import \
    GoalInstrumentation
from goal_service.domain.messages.command import SetGoalCommand
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

    def setUp(self):
        self.factory = mock(create_goal)
        self.repository = mock(Repository)
        self.instrument = mock(GoalInstrumentation)

        when(self.factory).__call__(**self.A_GOAL_JSON).thenReturn(self.A_GOAL)
        when(self.instrument).goal_set(self.A_GOAL).thenReturn(None)
        when(self.repository).add(self.A_GOAL).thenReturn(None)

    def test_set_goal(self):

        # Given
        command = SetGoalCommand(
            name=self.A_GOAL_NAME,
            description=self.A_GOAL_DESCRIPTION,
            due_date=self.A_GOAL_DUE_DATE)

        # When
        handler = SetGoalCommandHandler(
            factory=self.factory,
            repository=self.repository,
            instrumentation=self.instrument)
        handler(command)

        # Then
        verify(self.factory, times=1).__call__(**self.A_GOAL_JSON)
        verify(self.repository, times=1).add(self.A_GOAL)
        verify(self.instrument, times=1).goal_set(self.A_GOAL)
