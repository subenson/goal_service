from domain.model.goal import GoalRegistry, Goal


class InMemoryGoalRegistry(GoalRegistry):

    def __init__(self):
        self._registry = list()

    def add(self, goal: Goal) -> None:
        self._registry.append(goal)

    def __len__(self):
        return len(self._registry)
