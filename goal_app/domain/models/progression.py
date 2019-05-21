from datetime import datetime

from goal_app.domain.models import Entity


class Progression(Entity):

    def __init__(self, note, percentage):
        super().__init__()
        self._note = note
        self._percentage = percentage
        self._datetime = datetime.now()

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
        self._percentage = percentage


def create_progression(note, percentage):
    return Progression(note=note, percentage=percentage)
