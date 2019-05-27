import unittest
from datetime import datetime

from mockito import mock, when, verify

from goal_service.application.handlers.command import SetGoalCommandHandler, \
    CompleteGoalCommandHandler, DiscardGoalCommandHandler
from goal_service.application.instrumentation.goal.instrumentation import \
    GoalInstrumentation
from goal_service.domain.messages.command import SetGoalCommand, \
    CompleteGoalCommand, DiscardGoalCommand
from goal_service.infrastructure.repositories.goal import \
    InMemoryGoalRepository
from goal_service.domain.models.goal import Goal, create_goal
from goal_service.domain.models import DiscardedEntityException


class TestGoalCommandHandler(unittest.TestCase):

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

    A_DISCARDED_GOAL = mock({
        "id": A_GOAL_ID,
        "discarded": True
    }, spec=Goal)

    def setUp(self):
        self.factory = mock(create_goal)
        self.repository = InMemoryGoalRepository()
        self.instrumentation = mock(GoalInstrumentation)

    def test_set_goal_should_add_new_goal_to_the_repository(self):
        when(self.factory).__call__(**self.A_GOAL_JSON).thenReturn(self.A_GOAL)
        when(self.instrumentation).goal_set(self.A_GOAL).thenReturn(None)

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
        assert len(self.repository) == 1

    def test_complete_goal_should_flag_goal_as_completed(self):
        when(self.instrumentation).goal_completed(self.A_GOAL).thenReturn(None)
        when(self.factory).__call__(**self.A_GOAL_JSON).thenReturn(self.A_GOAL)
        when(self.A_GOAL).complete().thenReturn(None)

        # Given
        self.repository.add(self.A_GOAL)
        command = CompleteGoalCommand(id=self.A_GOAL_ID)

        # When
        handler = CompleteGoalCommandHandler(
            repository=self.repository,
            instrumentation=self.instrumentation)
        handler(command)

        # Then
        verify(self.A_GOAL, times=1).complete()

    def test_complete_discarded_goal_should_raise_exception(self):
        when(self.A_DISCARDED_GOAL).complete().thenRaise(
            DiscardedEntityException)

        # Given
        self.repository.add(self.A_DISCARDED_GOAL)
        command = CompleteGoalCommand(id=self.A_GOAL_ID)

        # When
        with self.assertRaises(DiscardedEntityException):
            handler = CompleteGoalCommandHandler(
                repository=self.repository,
                instrumentation=self.instrumentation)
            handler(command)

    def test_discard_goal_should_flag_goal_as_discarded(self):
        when(self.instrumentation).goal_discarded(self.A_GOAL).thenReturn(None)
        when(self.factory).__call__(**self.A_GOAL_JSON).thenReturn(self.A_GOAL)
        when(self.A_GOAL).discard().thenReturn(None)

        # Given
        self.repository.add(self.A_GOAL)
        command = DiscardGoalCommand(id=self.A_GOAL_ID)

        # When
        handler = DiscardGoalCommandHandler(
            repository=self.repository,
            instrumentation=self.instrumentation)
        handler(command)

        # Then
        verify(self.A_GOAL, times=1).discard()

    def test_discard_discarded_goal_should_raise_exception(self):
        when(self.A_DISCARDED_GOAL).discard().thenRaise(
            DiscardedEntityException)

        # Given
        self.repository.add(self.A_DISCARDED_GOAL)
        command = CompleteGoalCommand(id=self.A_GOAL_ID)

        # When
        with self.assertRaises(DiscardedEntityException):
            handler = DiscardGoalCommandHandler(
                repository=self.repository,
                instrumentation=self.instrumentation)
            handler(command)
