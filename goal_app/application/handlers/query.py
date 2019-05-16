class Query:
    def __init__(self, session):
        self._session = session


class ListOpenGoalsQuery(Query):
    def __call__(self):
        result = self._session.execute(
            'SELECT id, name, description, due_date FROM goal WHERE '
            'completed = False and discarded = False')
        return [dict(r) for r in result.fetchall()]


class ListProgressionsQuery(Query):
    def __call__(self, goal_id):
        result = self._session.execute(
            'SELECT id, note, percentage, datetime FROM goal_progression '
            'WHERE discarded = False AND goal_id = "%s"'
            'ORDER BY datetime DESC' % goal_id)
        return [dict(r) for r in result.fetchall()]
