from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def guess(self):
        pass

    @abstractmethod
    def update_guess(self, prev_guess: int, was_prev_guess_low: bool) -> None:
        pass