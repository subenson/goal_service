from sqlalchemy.orm import mapper, relationship

from goal_service.domain.models.goal import Goal
from goal_service.domain.models.progression import Progression


class DatabaseMapping:

    def __init__(self, goal_table, goal_progression_table):
        mapper(Goal, goal_table, properties={
            '_id': goal_table.c.id,
            '_name': goal_table.c.name,
            '_description': goal_table.c.description,
            '_due_date': goal_table.c.due_date,
            '_main_goal_id': goal_table.c.main_goal_id,
            '_completed': goal_table.c.completed,
            '_discarded': goal_table.c.discarded,
            'progressions': relationship(Progression),
            'subgoals': relationship(Goal)})
        mapper(Progression, goal_progression_table, properties={
            '_id': goal_progression_table.c.id,
            '_note': goal_progression_table.c.note,
            '_percentage': goal_progression_table.c.percentage,
            '_goal_id': goal_progression_table.c.goal_id,
            '_datetime': goal_progression_table.c.datetime,
            '_discarded': goal_progression_table.c.discarded})
