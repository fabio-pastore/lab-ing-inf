from store_item.GenericItem import GenericItem

class ForeignItem(GenericItem):
    def __init__(self, name: str, price: float):
        super().__init__(name, price)

    def get_price(self) -> float:
        return 1.2 * self.price

    def __str__(self) -> str:
        return ("{ID: " + str(self.id) + ", NAME: '" + self.name + "', PRICE: " + str(self.price) + " [FOREIGN]}")
