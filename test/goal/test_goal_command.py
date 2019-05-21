import unittest
from datetime import datetime

from mockito import mock, when

from goal_app.application.handlers.command import SetGoalCommandHandler, \
    CompleteGoalCommandHandler, DiscardGoalCommandHandler
from goal_app.application.instrumentation.goal import FakeGoalInstrumentation, \
    GoalInstrumentation
from goal_app.domain.messages.command import SetGoalCommand, \
    CompleteGoalCommand, DiscardGoalCommand
from goal_app.infrastructure.repositories.goal import InMemoryGoalRepository
from goal_app.domain.models.goal import Goal, create_goal
from goal_app.domain.models import DiscardedEntityException


class TestGoal(unittest.TestCase):

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
        self.repository = InMemoryGoalRepository()
        self.instrumentation = mock(GoalInstrumentation)

        when(self.factory).__call__(**self.A_GOAL_JSON).thenReturn(self.A_GOAL)
        when(self.instrumentation).goal_set(self.A_GOAL).thenReturn(None)

    def test_set_goal_should_add_new_goal_to_the_repository(self):
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
        # Given
        goal = Goal(**self.A_GOAL_JSON)
        self.repository.add(goal)
        command = CompleteGoalCommand(id=goal.id)

        # When
        handler = CompleteGoalCommandHandler(
            repository=self.repository,
            instrumentation=FakeGoalInstrumentation)
        handler(command)

        # Then
        assert goal.completed

    def test_complete_discarded_goal_should_raise_exception(self):
        # Given
        goal = Goal(**self.A_GOAL_JSON)
        goal.discard()
        self.repository.add(goal)
        command = CompleteGoalCommand(id=goal.id)

        # When
        with self.assertRaises(DiscardedEntityException):
            handler = CompleteGoalCommandHandler(
                repository=self.repository,
                instrumentation=FakeGoalInstrumentation)
            handler(command)

    def test_discard_goal_should_flag_goal_as_discarded(self):
        # Given
        goal = Goal(**self.A_GOAL_JSON)
        self.repository.add(goal)
        command = DiscardGoalCommand(id=goal.id)

        # When
        handler = DiscardGoalCommandHandler(
            repository=self.repository,
            instrumentation=FakeGoalInstrumentation)
        handler(command)

        # Then
        assert goal.discarded

    def test_discard_discarded_goal_should_raise_exception(self):
        # Given
        goal = Goal(**self.A_GOAL_JSON)
        goal.discard()
        self.repository.add(goal)
        command = DiscardGoalCommand(id=goal.id)

        # When
        with self.assertRaises(DiscardedEntityException):
            handler = DiscardGoalCommandHandler(
                repository=self.repository,
                instrumentation=FakeGoalInstrumentation)
            handler(command)
