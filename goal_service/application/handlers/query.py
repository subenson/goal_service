class Query:
    def __init__(self, session):
        self._session = session


class ListOpenGoalsQuery(Query):
    def __call__(self, main_goal_id=None):
        count_subquery = """(
            SELECT COUNT(*) FROM goal WHERE main_goal_id = g.id) AS subgoals"""

        query = f"""
            SELECT id, name, description, due_date, {count_subquery}
            FROM goal g 
            WHERE completed = False and discarded = False"""

        main_goal_filter = " and main_goal_id IS NULL"
        if main_goal_id:
            main_goal_filter = f" and main_goal_id = '{main_goal_id}'"

        query += main_goal_filter

        result = self._session.execute(query)
        return [dict(r) for r in result.fetchall()]


class ListProgressionsQuery(Query):
    def __call__(self, goal_id):
        result = self._session.execute(
            'SELECT id, note, percentage, datetime FROM goal_progression '
            'WHERE discarded = False AND goal_id = "%s"'
            'ORDER BY datetime DESC' % goal_id)
        return [dict(r) for r in result.fetchall()]
