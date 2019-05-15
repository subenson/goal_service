from datetime import datetime

from goal_app.domain.models import Entity


class Progression(Entity):

    def __init__(self, note, percentage):
        super().__init__()
        self._note = note
        self._percentage = percentage
        self._datetime = datetime.now()

    @property
    def note(self):
        return self._note

    @property
    def percentage(self):
        return self._percentage
