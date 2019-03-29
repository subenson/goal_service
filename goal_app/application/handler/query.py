class ListOpenGoalsQuery:

    def __init__(self, session):
        self._session = session

    def __call__(self):
        result = self._session.execute(
            'SELECT id, name, description, due_date FROM goal WHERE '
            'completed = False and discarded = False')
        return [dict(r) for r in result.fetchall()]
