import unittest
from datetime import datetime

from application.handler.command import SetGoalCommandHandler
from domain.message.command import SetGoalCommand
from infrastructure.adapter.orm.goal import InMemoryGoalRepository


class TestGoal(unittest.TestCase):

    A_GOAL_NAME = "Read a book this week"
    A_GOAL_DESCRIPTION = "7 Habits of Highly Effective People"
    A_GOAL_DUE_DATE = datetime.now()

    def setUp(self):
        self.goal_registry = InMemoryGoalRepository()

    def test_set_goal_should_add_new_goal_to_the_registry(self):
        # Given
        command = SetGoalCommand(
            name=self.A_GOAL_NAME,
            description=self.A_GOAL_DESCRIPTION,
            due_date=self.A_GOAL_DUE_DATE)

        # When
        handler = SetGoalCommandHandler(registry=self.goal_registry)
        handler(command)

        # Then
        assert len(self.goal_registry) == 1
