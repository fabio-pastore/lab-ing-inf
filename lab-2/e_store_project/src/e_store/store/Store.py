from store.store_inventory.StoreInventory import StoreInventory
from store_item.ForeignItem import ForeignItem
from store_item.GenericItem import GenericItem

class Store():
    def __init__(self, item_stock: StoreInventory, funds: float):
        if isinstance(item_stock, StoreInventory):
            self.item_stock = item_stock
            self.funds = funds

    def add_item(self, item: GenericItem):
        self.item_stock.add_item(item)

    def sell_item(self, item: GenericItem):
        self.item_stock.remove_item(item)
        if (isinstance(item, ForeignItem)):
            self.funds += (item.price + 0.2 * item.price)
        else:
            self.funds += item.price

    def show_items(self):
        print("<===================== STORE INVENTORY =====================>")
        for item in set(self.item_stock.item_list.keys()):
            if isinstance(item, ForeignItem):
                print("| ITEM: " + str(item) + " | PRICE: " + str(1.2 * item.price) + " | AVAILABLE_QUANTITY: " + str(self.item_stock.item_list[item]))
            else:
                print("| ITEM: " + str(item) + " | PRICE: " + str(item.price) + " | AVAILABLE_QUANTITY: " + str(self.item_stock.item_list[item]))
        print("<===========================================================>")

    def search_item(self, item_id: int) -> GenericItem:
        """
        This function searches the store inventory for the item with id 'item_id'. 

        search_item() compares the values saved in the dictionary 'self.item_stock' to see if some key of the dictionary (item) has id 'item_id', and returns
        such item if a match is found.

        Args:
            item_id (int): the ID of the item we are searching for

        Returns:
            GenericCustomer if search successful, otherwise None is returned.
        """
        for i in set(self.item_stock.item_list.keys()):
            if i.id == item_id:
                return i
        else: 
            return None
