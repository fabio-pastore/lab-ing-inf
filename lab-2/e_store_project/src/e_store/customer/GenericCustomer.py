from abc import ABC, abstractmethod

class GenericCustomer(ABC):
    @abstractmethod
    def __init__(self, name: str, funds: float, pwd: str):
        self.name = name
        self.funds = funds
        self.pwd = pwd