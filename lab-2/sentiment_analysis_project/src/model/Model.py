from abc import ABC, abstractmethod

class Model(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def analyze(self, review_data: list[tuple[str, int]]) -> None:
        pass

    @abstractmethod
    def predict(self, review: str) -> int:
        pass
