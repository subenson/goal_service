from abc import ABC, abstractmethod


class ProgressionMetrics(ABC):

    @abstractmethod
    def progression_added(self):
        raise NotImplementedError

    @abstractmethod
    def progression_discarded(self):
        raise NotImplementedError

    @abstractmethod
    def progression_edited(self):
        raise NotImplementedError


class InMemoryProgressionMetrics(ProgressionMetrics):

    def __init__(self):
        self.progressions_added = 0
        self.progressions_discarded = 0
        self.progressions_edited = 0

    def progression_added(self):
        self.progressions_added += 1

    def progression_discarded(self):
        self.progressions_discarded += 1

    def progression_edited(self):
        self.progressions_edited += 1
