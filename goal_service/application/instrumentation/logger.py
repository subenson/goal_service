from abc import ABC, abstractmethod


class Logger(ABC):

    @abstractmethod
    def log(self, message):
        raise NotImplementedError


class ConsoleLogger(Logger):

    def log(self, message):
        print(message)
