import requests, json

from .yoguide import *

class ItemSearch:
    @staticmethod
    def ywdbSearch(item: Item) -> None:
        heads = {"Content-Type": "application/x-www-form-urlencoded"};
        id = {"iid": f"{item.id}"};
        results = requests.post("https://yoworlddb.com/scripts/getItemInfo.php", headers=heads, data=id).text;

        if not results.startswith("{") or not results.endswith("}"):
            print(f"[ X ] (INVALID_JSON) Error, Unable to get item information....!\n\n{results}");
            return;

        info = json.loads(results)['response'];

        item.gender = info['gender']
        item.is_tradable = info['is_tradable'];
        item.is_free_gift = info['can_gift'];
        item.category = info['category'];
        item.xp = info['xp'];

        if info['active_in_store'] == "1": item.in_store = True;
        else: item.in_store = False;

        if info['price_coins'] != "0": item.store_price = f"{info['price_coins']}c";
        elif info['price_cash'] != "0": item.store_price = f"{info['price_cash']}yc"
        else: item.store_price = "0";
        
        return item;