import unittest
from datetime import datetime

from goal_app.application.handler.command import SetGoalCommandHandler, \
    CompleteGoalCommandHandler, DiscardGoalCommandHandler
from goal_app.domain.message.command import SetGoalCommand, \
    CompleteGoalCommand, DiscardGoalCommand
from goal_app.infrastructure.repositories.goal import InMemoryGoalRepository
from goal_app.domain.model.goal import Goal
from goal_app.domain.model import DiscardedEntityException


class TestGoal(unittest.TestCase):

    A_GOAL_NAME = "Read a book this week"
    A_GOAL_DESCRIPTION = "7 Habits of Highly Effective People"
    A_GOAL_DUE_DATE = datetime.now()

    A_GOAL_JSON = {
        "name": A_GOAL_NAME,
        "description": A_GOAL_DESCRIPTION,
        "due_date": A_GOAL_DUE_DATE
    }

    def setUp(self):
        self.repository = InMemoryGoalRepository()

    def test_set_goal_should_add_new_goal_to_the_repository(self):
        # Given
        command = SetGoalCommand(
            name=self.A_GOAL_NAME,
            description=self.A_GOAL_DESCRIPTION,
            due_date=self.A_GOAL_DUE_DATE)

        # When
        handler = SetGoalCommandHandler(repository=self.repository)
        handler(command)

        # Then
        assert len(self.repository) == 1

    def test_complete_goal_should_flag_goal_as_completed(self):
        # Given
        goal = Goal(**self.A_GOAL_JSON)
        self.repository.add(goal)
        command = CompleteGoalCommand(id=goal.id)

        # When
        handler = CompleteGoalCommandHandler(repository=self.repository)
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
            handler = CompleteGoalCommandHandler(repository=self.repository)
            handler(command)

    def test_discard_goal_should_flag_goal_as_discarded(self):
        # Given
        goal = Goal(**self.A_GOAL_JSON)
        self.repository.add(goal)
        command = DiscardGoalCommand(id=goal.id)

        # When
        handler = DiscardGoalCommandHandler(repository=self.repository)
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
            handler = DiscardGoalCommandHandler(repository=self.repository)
            handler(command)
