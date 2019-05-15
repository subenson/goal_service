import unittest
from datetime import datetime

from goal_app.application.handler.command import \
    SetGoalProgressionCommandHandler
from goal_app.domain.message.command import SetGoalProgressionCommand
from goal_app.infrastructure.orm.goal import InMemoryGoalRepository
from goal_app.domain.model.goal import Goal


class TestGoal(unittest.TestCase):

    A_GOAL_NAME = "Read a book this week"
    A_GOAL_DESCRIPTION = "7 Habits of Highly Effective People"
    A_GOAL_DUE_DATE = datetime.now()

    A_GOAL = Goal(**{
        "name": A_GOAL_NAME,
        "description": A_GOAL_DESCRIPTION,
        "due_date": A_GOAL_DUE_DATE
    })

    A_PROGRESSION_NOTE = "I read 60 of the 100 pages. It really is a " \
                         "fantastic book!"
    A_PROGRESSION_PERCENTAGE = 60

    def setUp(self):
        self.repository = InMemoryGoalRepository()
        self.repository.add(self.A_GOAL)

    def test_set_progression_should_add_new_progression_to_the_goal(self):
        # Given
        A_GOAL = self.repository._registry[0]

        command = SetGoalProgressionCommand(
            goal_id=A_GOAL.id,
            note=self.A_PROGRESSION_NOTE,
            percentage=self.A_PROGRESSION_PERCENTAGE)

        # When
        handler = SetGoalProgressionCommandHandler(repository=self.repository)
        handler(command)

        # Then
        # Get a fresh instance from the repository
        goal = self.repository.get(id_=A_GOAL.id)

        assert len(goal.progressions) == 1
        assert goal.progressions[0].note == self.A_PROGRESSION_NOTE
        assert goal.progressions[0].percentage == self.A_PROGRESSION_PERCENTAGE
