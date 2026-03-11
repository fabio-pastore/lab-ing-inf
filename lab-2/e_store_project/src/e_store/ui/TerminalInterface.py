from store.Store import Store
from customer.GenericCustomer import GenericCustomer
from customer.PromotionalCustomer import PromotionalCustomer
from store_item.ForeignItem import ForeignItem

class TerminalInterface:
    def __init__(self, store: Store, customers: list[GenericCustomer]):
        if isinstance(store, Store) and isinstance(customers, list) and all(isinstance(c, GenericCustomer) for c in customers):
            self.store = store
            self.customers = customers

    def login(self) -> GenericCustomer:
        """
        This function requests the user to provide information (username, password) to log into the system. 

        Two checks are performed. First, we must check if a user with name 'username' exists in the system. If such user exists, login() checks if the saved
        password for that user is exactly equal to the user input.

        Args:
            --

        Returns:
            GenericCustomer if login successful, otherwise None is returned.
        """
        while True:
                customer = None
                username = input("$ store-manager >> USERNAME >> ")
                for user in self.customers:
                    if user.name == username:
                        customer = user
                pwd = input("$ store-manager >> PWD >> ")
                if (customer is None or not (customer.pwd == pwd)):
                    print("Invalid username or password.")
                    print()
                    continue
                print("Successfully logged in. Welcome " + username + "!")
                break
        return customer

    def start_app(self):

        print("$ STORE-MANAGER v1.0 by Fabio")
        print("Please log into your account.")
        customer = self.login()

        while True:
            print("Store balance: " + str(self.store.funds))
            self.store.show_items()
            print("Available balance: " + str(customer.funds))
            print("Please insert ID of item to buy (or QUIT to exit the app).")
            recv_input = input("$ store-manager ")
            if (recv_input.lower() == "quit"):
                print("Exiting process with exit code (0)")
                break

            item_id = int(recv_input)
            req_item = self.store.search_item(item_id)
            if req_item is None:
                print("Could not find specified item. Please try again.")
                continue 

            if (self.store.item_stock.item_list[req_item] == 0):
                print("The selected item is currently unavailable. Please try again later.")
                continue

            print("Please insert desired quantity.")
            req_qty = int(input("$ store-manager "))
            if self.store.item_stock.item_list[req_item] < req_qty:
                print("The store cannot satisfy the requested amount. Please try with a lower quantity or pick another item.")
                continue

            print("Successfully selected item with ID: " + str(item_id) + ". Requested quantity: " + str(req_qty) + ".")
             
            print("Balance: " + str(customer.funds))
            if (isinstance(req_item, ForeignItem)):
                print("NOTE: the purchase contains an additional 20% fee due to international shipment.")
            
            promo_user = False
            item_c = req_item.get_price()
            tot_c = req_qty * item_c
            if (isinstance(customer, PromotionalCustomer)):
                    tot_c = 0.95 * tot_c
                    promo_user = True
                    print("Promotional client discount applied successfully!")
            print("Total cost: " + str(round(tot_c, 2)))
            print("Please confirm or cancel the current order. Y/N")
            choice = input("$ store-manager ")
            if (choice.lower() == 'n'):
                print("Transaction successfully aborted.")
                continue

            elif (choice.lower() == 'y'):
                
                if tot_c > customer.funds:
                    print("Could not complete transaction! Insufficient funds.")
                    continue
                customer.funds -= tot_c
                for j in range(req_qty):
                    self.store.sell_item(req_item, promo_user)
                print("Transaction completed successfully.")

            else:
                print("Invalid choice!")
                continue



