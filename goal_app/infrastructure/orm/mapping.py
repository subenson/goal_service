from sqlalchemy.orm import mapper, relationship

from goal_app.infrastructure.orm.schema import GOAL_TABLE, \
    GOAL_PROGRESSION_TABLE
from goal_app.domain.models.goal import Goal
from goal_app.domain.models.progression import Progression

mapper(Goal, GOAL_TABLE, properties={
    '_id': GOAL_TABLE.c.id,
    '_name': GOAL_TABLE.c.name,
    '_description': GOAL_TABLE.c.description,
    '_due_date': GOAL_TABLE.c.due_date,
    '_completed': GOAL_TABLE.c.completed,
    '_discarded': GOAL_TABLE.c.discarded,
    'progressions': relationship(Progression)})

mapper(Progression, GOAL_PROGRESSION_TABLE, properties={
    '_id': GOAL_PROGRESSION_TABLE.c.id,
    '_note': GOAL_PROGRESSION_TABLE.c.note,
    '_percentage': GOAL_PROGRESSION_TABLE.c.percentage,
    '_goal_id': GOAL_PROGRESSION_TABLE.c.goal_id,
    '_datetime': GOAL_PROGRESSION_TABLE.c.datetime,
    '_discarded': GOAL_PROGRESSION_TABLE.c.discarded})
