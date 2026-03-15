import random

class StoreItems():

    ITEM_ID = 1

    def __init__(self):
        self.items = {}

    def store_item(self, item):
        # unique_id = random.randint(1, 100_000) this does not guarantee a unique_id!
        unique_id = StoreItems.ITEM_ID
        self._increase_item_id_counter()
        self.items[unique_id] = item
        return unique_id

    # this method was added to increate the item_id counter
    @classmethod 
    def _increase_item_id_counter(cls):
        cls.ITEM_ID += 1

    def retrieve_item(self, unique_id):
        return self.items.get(unique_id, "Item not found")

    def pretty_print(self):
        if not self.items:
            print("No items stored.")
        else:
            print("Stored Items:")
            for key, value in self.items.items():
                print(f"ID: {key} -> Item: {value}")

    def random_choice(self):
        return random.choice(list(self.items.values()))

    def delete_item(self, unique_id):
        return self.items.pop(unique_id)

    def item_exists(self, unique_id):
        return unique_id in self.items # used to be self.items.values()

    def get_all_items(self):
        return self.items

    def count_items(self):
        return len(self.items)

    def clear_items(self):
        self.items.clear()
        return "All items have been cleared."

    def get_all_ids(self):
        return list(self.items.keys())
    