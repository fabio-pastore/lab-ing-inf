from store_item.GenericItem import GenericItem

class StoreInventory:
    def __init__(self):
        self.item_list = {}

    def add_item(self, item: GenericItem, qty: int):
        if isinstance(item, GenericItem):
            if item in self.item_list:
                self.item_list[item] += qty
            else:
                self.item_list[item] = qty
    
    def remove_item(self, item: GenericItem):
        if isinstance(item, GenericItem) and item in set(self.item_list.keys()):
            if (self.item_list[item] == 0):
                raise Exception("Selected item is not available.")
            else:
                self.item_list[item] -= 1


