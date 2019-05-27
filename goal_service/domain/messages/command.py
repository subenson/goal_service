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


class AddProgressionCommand(NamedTuple):
    goal_id: uuid.uuid4
    note: str
    percentage: int


class DiscardProgressionCommand(NamedTuple):
    id: uuid.uuid4


class EditProgressionCommand(NamedTuple):
    id: uuid.uuid4
    note: str
    percentage: int


class SetSubGoalCommand(NamedTuple):
    name: str
    description: str
    due_date: datetime
    main_goal_id: str
