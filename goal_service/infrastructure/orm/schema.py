# pylint: disable=bad-continuation
from sqlalchemy import Table, Column, String, DateTime, Boolean, Integer, \
    ForeignKey
from . import database


GOAL_TABLE = Table('goal', database.metadata,
    Column('id', String(36), primary_key=True),
    Column('name', String),
    Column('description', String),
    Column('due_date', DateTime(timezone=True)),
    Column('main_goal_id', String(36), ForeignKey("goal.id")),
    Column('completed', Boolean),
    Column('discarded', Boolean))

GOAL_PROGRESSION_TABLE = Table(
    'goal_progression',
    database.metadata,
    Column('id', String(36), primary_key=True),
    Column('note', String),
    Column('percentage', Integer),
    Column('datetime', DateTime(timezone=True)),
    Column('discarded', Boolean),
    Column('goal_id', String(36), ForeignKey("goal.id"), nullable=False))
