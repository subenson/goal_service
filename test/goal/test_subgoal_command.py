import unittest
from datetime import datetime

from mockito import mock, when

from goal_service.application.handlers.command import SetSubGoalCommandHandler
from goal_service.application.instrumentation.goal.instrumentation import \
    GoalInstrumentation
from goal_service.domain.messages.command import SetSubGoalCommand
from goal_service.infrastructure.repositories.goal import \
    InMemoryGoalRepository
from goal_service.domain.models.goal import Goal, create_goal


class TestGoalCommandHandler(unittest.TestCase):

    A_MAIN_GOAL_ID = "22345673-5678-9012-1234-323456789011"

    A_MAIN_GOAL = Goal(**{
        "name": "",
        "description": "",
        "due_date": ""
    })

    A_GOAL_ID = "12345678-1234-5678-9012-123456789012"
    A_GOAL_NAME = "Read a book this week"
    A_GOAL_DESCRIPTION = "7 Habits of Highly Effective People"
    A_GOAL_DUE_DATE = datetime.now()

    A_GOAL_JSON = {
        "name": A_GOAL_NAME,
        "description": A_GOAL_DESCRIPTION,
        "due_date": A_GOAL_DUE_DATE
    }

    A_GOAL = Goal(**{
        "name": A_GOAL_NAME,
        "description": A_GOAL_DESCRIPTION,
        "due_date": A_GOAL_DUE_DATE
    })

    def setUp(self):
        self.factory = create_goal
        self.repository = InMemoryGoalRepository()
        self.instrumentation = mock(GoalInstrumentation)
        when(self.instrumentation).goal_set(...).thenReturn(None)

        self.A_MAIN_GOAL._id = self.A_MAIN_GOAL_ID
        self.A_GOAL._id = self.A_GOAL_ID

    def test_set_subgoal_command_should_add_new_subgoal(self):
        self.repository.add(self.A_MAIN_GOAL)

        # Given
        command = SetSubGoalCommand(
            name=self.A_GOAL_NAME,
            description=self.A_GOAL_DESCRIPTION,
            due_date=self.A_GOAL_DUE_DATE,
            main_goal_id=self.A_MAIN_GOAL_ID)

        # When
        handler = SetSubGoalCommandHandler(
            factory=self.factory,
            repository=self.repository,
            instrumentation=self.instrumentation)
        handler(command)

        # Then
        assert len(self.A_MAIN_GOAL.subgoals) == 1
