from sqlalchemy.orm import mapper, relationship

from goal_service.domain.models.goal import Goal
from goal_service.domain.models.progression import Progression


class DatabaseMapping:

    def __init__(self, schema):
        mapper(Goal, schema.goal, properties={
            '_id': schema.goal.c.id,
            '_name': schema.goal.c.name,
            '_description': schema.goal.c.description,
            '_due_date': schema.goal.c.due_date,
            '_main_goal_id': schema.goal.c.main_goal_id,
            '_completed': schema.goal.c.completed,
            '_discarded': schema.goal.c.discarded,
            'progressions': relationship(Progression),
            'subgoals': relationship(Goal)})
        mapper(Progression, schema.goal_progression, properties={
            '_id': schema.goal_progression.c.id,
            '_note': schema.goal_progression.c.note,
            '_percentage': schema.goal_progression.c.percentage,
            '_goal_id': schema.goal_progression.c.goal_id,
            '_datetime': schema.goal_progression.c.datetime,
            '_discarded': schema.goal_progression.c.discarded})
