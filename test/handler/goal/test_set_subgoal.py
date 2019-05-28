import unittest
from datetime import datetime

from mockito import mock, when, verify

from goal_service.application.handlers import RelatedEntityNotFoundException
from goal_service.application.handlers.command import SetSubGoalCommandHandler
from goal_service.application.instrumentation.goal.interface import \
    GoalInstrumentation
from goal_service.domain.messages.command import SetSubGoalCommand
from goal_service.domain.models.goal import Goal, create_goal
from goal_service.domain.port import Repository
from goal_service.infrastructure.repositories import EntityNotFoundException


class TestGoalCommandHandler(unittest.TestCase):

    A_MAIN_GOAL_ID = "22345673-5678-9012-1234-323456789011"
    A_MAIN_GOAL = mock({
        "id": A_MAIN_GOAL_ID
    }, spec=Goal)

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
        self.instrumentation = mock(GoalInstrumentation)

        when(self.factory).__call__(**self.A_GOAL_JSON).thenReturn(self.A_GOAL)

    def test_set_subgoal(self):
        # Given
        command = SetSubGoalCommand(
            name=self.A_GOAL_NAME,
            description=self.A_GOAL_DESCRIPTION,
            due_date=self.A_GOAL_DUE_DATE,
            main_goal_id=self.A_MAIN_GOAL_ID)

        when(self.repository).get(self.A_MAIN_GOAL_ID).thenReturn(
            self.A_MAIN_GOAL)
        when(self.instrumentation).goal_set(self.A_GOAL).thenReturn(None)
        when(self.A_MAIN_GOAL).set_subgoal(self.A_GOAL).thenReturn(None)

        # When
        handler = SetSubGoalCommandHandler(
            factory=self.factory,
            repository=self.repository,
            instrumentation=self.instrumentation)
        handler(command)

        # Then
        verify(self.A_MAIN_GOAL, times=1).set_subgoal(self.A_GOAL)
        verify(self.repository, times=1).get(self.A_MAIN_GOAL_ID)
        verify(self.instrumentation, times=1).goal_set(self.A_GOAL)

    def test_set_subgoal_lookup_failed(self):
        # Given
        command = SetSubGoalCommand(
            name=self.A_GOAL_NAME,
            description=self.A_GOAL_DESCRIPTION,
            due_date=self.A_GOAL_DUE_DATE,
            main_goal_id=self.A_MAIN_GOAL_ID)

        when(self.repository).get(self.A_MAIN_GOAL_ID).thenRaise(
            EntityNotFoundException)
        when(self.instrumentation).goal_lookup_failed(
            self.A_MAIN_GOAL_ID).thenReturn(None)

        # When
        with self.assertRaises(RelatedEntityNotFoundException):
            handler = SetSubGoalCommandHandler(
                factory=self.factory,
                repository=self.repository,
                instrumentation=self.instrumentation)
            handler(command)

        # Then
        verify(self.instrumentation, times=1).goal_lookup_failed(
            self.A_MAIN_GOAL_ID)
