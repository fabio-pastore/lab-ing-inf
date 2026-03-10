from ui.TerminalInterface import TerminalInterface
from customer.NormalCustomer import NormalCustomer
from customer.PromotionalCustomer import PromotionalCustomer
from store_item.NormalItem import NormalItem
from store_item.ForeignItem import ForeignItem
from store.Store import Store
from store.store_inventory.StoreInventory import StoreInventory

if __name__ == "__main__":
    
    inv = StoreInventory()
    i1 = NormalItem("Book", 5)
    i2 = NormalItem("Fridge", 150)
    i3 = ForeignItem("Videogame", 60)
    c1 = NormalCustomer("Fabio", 0, "123")
    c2 = PromotionalCustomer("Mark", 2000, "0000")
    inv.add_item(i1, 3)
    inv.add_item(i2, 1)
    inv.add_item(i3, 1)
    customer_list = [c1, c2]
    s = Store(inv, 500)
    t = TerminalInterface(s, customer_list)
    t.start_app()

    exit(0)

