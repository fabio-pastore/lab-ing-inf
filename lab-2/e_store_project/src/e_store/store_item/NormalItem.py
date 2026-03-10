from store_item.GenericItem import GenericItem

class NormalItem(GenericItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)

    def __str__(self) -> str:
        return ("{ID: " + str(self.id) + ", NAME: '" + self.name + "', PRICE: " + str(self.price) + "}")