from datetime import datetime

from goal_service.domain.models import Entity


class InvalidPercentageException(Exception):
    """Indicates that a invalid percentage is provided."""
    def __str__(self):
        return "invalid_percentage"


class Progression(Entity):

    def __init__(self, note, percentage):
        super().__init__()
        self._note = note
        self._percentage = None
        self._datetime = datetime.now()
        self.percentage = percentage  # Use setter

    @property
    def note(self) -> str:
        return self._note

    @note.setter
    def note(self, note: str):
        self._note = note

    @property
    def percentage(self) -> int:
        return self._percentage

    @percentage.setter
    def percentage(self, percentage: int):
        if not 0 <= percentage <= 100:
            raise InvalidPercentageException()
        self._percentage = percentage


def create_progression(note, percentage):
    return Progression(note=note, percentage=percentage)
