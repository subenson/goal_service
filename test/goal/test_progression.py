import unittest
from goal_app.domain.models.progression import Progression, \
    InvalidPercentageException


class TestProgression(unittest.TestCase):

    def test_negative_progression_percentage(self):
        # Given
        A_NEGATIVE_PERCENTAGE = -1

        # When / Then
        with self.assertRaises(InvalidPercentageException):
            progression = Progression(**{
                "note": "",
                "percentage": A_NEGATIVE_PERCENTAGE
            })

    def test_invalid_progression_percentage(self):
        # Given
        A_OVER_HUNDRED_PERCENTAGE = 101

        # When / Then
        with self.assertRaises(InvalidPercentageException):
            progression = Progression(**{
                "note": "",
                "percentage": A_OVER_HUNDRED_PERCENTAGE
            })
