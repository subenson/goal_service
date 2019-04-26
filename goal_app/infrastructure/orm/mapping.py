from sqlalchemy.orm import mapper

from goal_app.infrastructure.orm.schema import GOAL_TABLE
from goal_app.domain.model.goal import Goal


mapper(Goal, GOAL_TABLE, properties={
    '_id': GOAL_TABLE.c.id,
    '_name': GOAL_TABLE.c.name,
    '_description': GOAL_TABLE.c.description,
    '_due_date': GOAL_TABLE.c.due_date,
    '_completed': GOAL_TABLE.c.completed,
    '_discarded': GOAL_TABLE.c.discarded})
