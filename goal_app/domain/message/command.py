import uuid
from typing import NamedTuple
from datetime import datetime


class SetGoalCommand(NamedTuple):
    name: str
    description: str
    due_date: datetime


class CompleteGoalCommand(NamedTuple):
    id: uuid.uuid4


class DiscardGoalCommand(NamedTuple):
    id: uuid.uuid4


class SetGoalProgressionCommand(NamedTuple):
    goal_id: uuid.uuid4
    note: str
    percentage: int


class DiscardGoalProgressionCommand(NamedTuple):
    id: uuid.uuid4
