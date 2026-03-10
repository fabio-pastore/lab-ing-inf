from abc import ABC, abstractmethod

class GenericItem(ABC):

    id_counter = 100000
    
    @abstractmethod
    def __init__(self, name: str, price: float):
        self.id = GenericItem.id_counter
        GenericItem.id_counter += 1
        self.name = name
        self.price = price

    @abstractmethod
    def __str__(self) -> str:
        pass