import requests, json

from src.yoguide.yoguide import Item

class Search():
    def __init__(self, q: str):
        self.query = q;

    def __ywInfoSearch(self, i: Item) -> Item:
        item_price = "";
        item_update = "";

        resp = requests.get(f"https://api.yoworld.info/api/items{self.query}");
        if resp.status_code != 200:
            return False, item_price, item_update;

        response = resp.text

        item_info = json.loads(response)['item']['price_proposals'];

        for item in item_info:
            value = item_info[item];

            # if item == "name": item[item] = value;
            if item == "price": i.ywInfo_price = value.replace("000000", "m");
            if item == "updated_at": 
                i.ywInfo_update = value;
                return i;
                
        return i;