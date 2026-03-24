from customer.GenericCustomer import GenericCustomer
from customer.NormalCustomer import NormalCustomer
from customer.PromotionalCustomer import PromotionalCustomer
from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel, field_validator # type: ignore
from store.Store import Store
from store.store_inventory.StoreInventory import StoreInventory
from store_item.GenericItem import GenericItem
from store_item.ForeignItem import ForeignItem
from store_item.NormalItem import NormalItem

inv: StoreInventory = StoreInventory()
i1: GenericItem = NormalItem("Book", 5)    
i2: GenericItem = NormalItem("Fridge", 150)
i3: GenericItem = ForeignItem("Videogame", 60)
c1: GenericCustomer = NormalCustomer("Fabio", 0, "123")
c1.items = {i1: 2, i2: 3}
c2: GenericCustomer = PromotionalCustomer("Mark", 2000, "0000")
inv.add_item(i1, 3)
inv.add_item(i2, 1)
inv.add_item(i3, 1)
customer_list: list[GenericCustomer] = [c1, c2]
s : Store = Store(inv, 500)

app = FastAPI()

class GenericItemModel(BaseModel):
    id: int
    name: str
    price: float

class ListItem(BaseModel):
    item: GenericItemModel
    quantity: int

class InventoryList(BaseModel):
    item_list: list[ListItem]
    
class UserInventoryList(BaseModel):
    items: list[ListItem]

class UserBalance(BaseModel):
    bal: float

class ItemInfo(BaseModel):
    price: float
    quantity: int

class PurchaseRequest(BaseModel):
    username: str
    password: str
    item_id: int
    quantity: int

    @field_validator("quantity") # type: ignore
    def validate_purchase_req(cls, field_val: int) -> int:
        if field_val <= 0:
            raise ValueError("quantity field must be positive")
        else:
            return field_val

class PurchaseConfirmation(BaseModel):
    total_price: float
    promo_discount: bool

def find_user(username: str) -> GenericCustomer | None:
    found_user: bool = None
    for c in customer_list:
        if c.name == username:
            found_user = c
    return found_user

@app.get("/get_inventory")
def display_inventory() -> InventoryList:
    item_list: list[tuple[GenericItem, int]] = s.get_items()
    out: list[ListItem] = []
    for pair in item_list:
        id, name = pair[0].id, pair[0].name
        gitem: GenericItemModel = GenericItemModel(id=id, name=name, price=pair[0].get_price())
        quantity: int = pair[1]
        out.append(ListItem(item=gitem, quantity=quantity))
    return InventoryList(item_list=out)

@app.get("/get_user_items/{username}")
def get_user_items(username: str) -> UserInventoryList:
    selected_user: GenericCustomer | None = find_user(username)
    if selected_user is None:
        raise HTTPException(status_code=404, detail="Username not found")
    user_items : list[ListItem] = []
    for key,value in selected_user.items.items():
        gitem: GenericItemModel = GenericItemModel(id=key.id, name=key.name, price=key.get_price())
        user_items.append(ListItem(item=gitem, quantity=value))
    return UserInventoryList(items=user_items)

@app.get("/get_item_information/{item_id}")
def get_item_info(item_id: int):
    selected_item: GenericItem | None = s.search_item(item_id)
    if selected_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemInfo(price=selected_item.get_price(), quantity=s.get_available_quantity(selected_item))

@app.get("/get_balance/{username}")
def get_user_balance(username: str) -> UserBalance:
    selected_user: GenericCustomer | None = find_user(username)
    if selected_user is None:
        raise HTTPException(status_code=404, detail="Username not found")
    return UserBalance(bal=selected_user.funds)
    
@app.post("/purchase")
def purchase_item(purchase_request: PurchaseRequest) -> PurchaseConfirmation:

    username: str = purchase_request.username
    pwd: str = purchase_request.password
    item_id: int = purchase_request.item_id
    item_qty: int = purchase_request.quantity

    selected_item: GenericItem | None = s.search_item(item_id)
    if selected_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    available_quantity: int = s.get_available_quantity(selected_item)
    if available_quantity < item_qty:
        raise HTTPException(status_code=406, detail="Item is present but not in the requested quantity")
    selected_user: GenericCustomer = find_user(username)
    if selected_user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not selected_user.pwd == pwd:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    is_promo_customer: bool = isinstance(selected_user, PromotionalCustomer)
    if is_promo_customer:
        purchase_cost: float = 0.95 * (item_qty * selected_item.get_price())
    else:
        purchase_cost: float = item_qty * selected_item.get_price()

    if purchase_cost > selected_user.funds:
        raise HTTPException(status_code=402, detail="Purchase could not be completed successfully: insufficient funds")

    for k in range(item_qty):
        s.sell_item(selected_item, is_promo_customer) # update store balance

    selected_user.funds -= purchase_cost
    if selected_item in selected_user.items:
        selected_user.items[selected_item] += item_qty
    else:
        selected_user.items[selected_item] = item_qty

    return PurchaseConfirmation(total_price=round(purchase_cost, 2), promo_discount=is_promo_customer)