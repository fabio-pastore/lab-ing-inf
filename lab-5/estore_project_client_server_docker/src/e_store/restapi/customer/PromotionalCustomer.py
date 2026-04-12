from customer.GenericCustomer import GenericCustomer

class PromotionalCustomer(GenericCustomer):
    def __init__(self, name: str, funds: float, pwd: str):
        super().__init__(name, funds, pwd)