import requests # type: ignore

class TerminalInterface:

    BASE_URL = "http://127.0.0.1:8000"

    def __init__(self):
        pass

    def validate_aux(self, recv_data) -> None | dict:
        data: None | dict = None
        if recv_data.status_code == 200:
            content_type = recv_data.headers.get("Content-Type", "")

            if "application/json" in content_type:
                try:
                    data: dict = recv_data.json()
                except ValueError:
                    print("$ store-manager: response does not contain a valid JSON!")
                
            else:
                print("$ store-manager : response is not JSON")
                print("Content-Type: " + str(content_type))
        
        else:
            print("$ store-manager: [HTTP_ERROR] > " + str(recv_data.status_code) + ": " + recv_data.json().get("detail"))

        return data

    def get_validated_data(self, url) -> None | dict:
        response: Response = requests.get(url) # type: ignore
        return self.validate_aux(response)

    def post_data(self, url, payload) -> None | dict:
        response: Response = requests.post(url, json=payload) # type: ignore
        return self.validate_aux(response)
        
    def get_inventory(self):
        req_url: str = TerminalInterface.BASE_URL + "/get_inventory"
        response_data: None | dict = self.get_validated_data(req_url)

        if response_data is None:
            print("$ store-manager: could not complete the selected operation.")
            return
        
        for elem in response_data.get("item_list"):
            item: dict = elem.get("item")
            quantity: str = elem.get("quantity")
            print(f"item_id: {item.get("id")} | item_name: {item.get("name")} | price: {item.get("price")} | quantity: {quantity}")

    def get_user_items(self):
        print("Please input user ID:")
        user_id: str = input("$ store-manager >> ")

        req_url: str = TerminalInterface.BASE_URL + f"/get_user_items/{user_id}"
        response_data: None | dict = self.get_validated_data(req_url)
        
        if response_data is None:
            print("$ store-manager: could not complete the selected operation.")
            return
        
        print(f"Found {len(response_data.get("items"))} items for user '{user_id}'")
        for elem in response_data.get("items"):
            item: dict = elem.get("item")
            quantity: str = elem.get("quantity")
            print(f"item_id: {item.get("id")} | item_name: {item.get("name")} | price: {item.get("price")} | quantity: {quantity}")

    def get_item_info(self):
        print("Please input item ID:")
        item_id: str = input("$ store-manager >> ")

        req_url: str = TerminalInterface.BASE_URL + f"/get_item_information/{item_id}"
        response_data: None | dict = self.get_validated_data(req_url)

        if response_data is None:
            print("$ store-manager: could not complete the selected operation.")
            return
        
        print(f"Found item with ID: {item_id}")
        print(f"price: {response_data.get("price")} | quantity: {response_data.get("quantity")}")

    def get_user_bal(self):
        print("Please input user ID:")
        user_id: str = input("$ store-manager >> ")

        req_url: str = TerminalInterface.BASE_URL + f"/get_balance/{user_id}"
        response_data: None | dict = self.get_validated_data(req_url)

        if response_data is None:
            print("$ store-manager: could not complete the selected operation.")
            return
        
        print(f"Balance of user '{user_id}' is: {response_data.get("bal")}")

    def purchase_item(self):

        print("Please input ID of item to purchase:")
        item_id: str = input("$ store-manager >> ")
        print("Please input desired quantity:")
        item_qty: str = input("$ store-manager >> ")
        print("$ store-manager: you will now be prompted to log-in in order to complete the purchase.")
        print("Please input user ID:")
        user_id: str = input("$ store-manager >> ")
        print("Please input your password:")
        user_pwd: str = input("$ store-manager >> ")
        
        req_url: str = TerminalInterface.BASE_URL + "/purchase"
        request_payload: dict = {
            "username": user_id,
            "password": user_pwd,
            "item_id": item_id,
            "quantity": item_qty
        }

        response_data: None | dict = self.post_data(req_url, request_payload)

        if response_data is None:
            print("$ store-manager: could not complete the selected operation.")
            return
        
        print("Purchase completed successfully. Order recap:")
        print(f"total_price: {response_data.get("total_price")} | promotional_discount: {"yes" if response_data.get("promo_discount") else "not applicable"}")

    def start_app(self):

        print("$ STORE-MANAGER v1.1 by Fabio")

        while True:
            id_choice: str = None
            print("Please insert desired operation (or QUIT to exit the app).")
            print("1. Get store inventory\n2. Get user items\n3. Get item information\n" +
                  "4. Get user balance\n5. Purchase item")
            try:
                id_choice = input("$ store-manager >> ")
                if not (1 <= int(id_choice) <= 5):
                    print("Invalid input. Please try again.")
                    print()
                    continue
            except ValueError:
                if id_choice.lower() == 'quit':
                    print("Received 'quit' command. Exiting app with status code (0).")
                    break
                else:
                    print("Choice must be a number (or 'QUIT'). Please try again.")
                    print()
                    continue
            
            match int(id_choice):
                case 1:
                    self.get_inventory()
                case 2:
                    self.get_user_items()
                case 3:
                    self.get_item_info()
                case 4:
                    self.get_user_bal()
                case 5:
                    self.purchase_item()
                case _:
                    print("Invalid input.") # NOTE: this will never be executed
                    continue