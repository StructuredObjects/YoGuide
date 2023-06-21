import requests, json

class Item():
    """
        General Item Information
    """
    name:   str;
    id:     int;
    url:    str;
    price:  str;
    update: str;

    """
        Actions you can do with the ITEM
    """
    is_tradable: int;
    is_giftable: int;

    """
        In-store Information
    """
    in_store:       bool;
    store_price:    str;
    gender:         str;
    xp:             str;
    categroy:       str;

class API:
    url = "https://api.yoguide.info"
    searchEndpoint = f"{url}/search"
    advanceEndpoint = f"{url}/advance"
    pricechangeEndpoint = f"{url}/change"


class YoGuide:
    @staticmethod
    def newItem(arr: list) -> Item:
        _item = Item();
        if len(arr) < 5: return Item();
        _item.name = arr[0]; _item.id = int(arr[1]); _item.url = arr[2];
        _item.price = arr[3]; _item.update = arr[4];

    @staticmethod
    def searchItems(item_name: str) -> list:
        found = [];
        results = requests.get(f"{API().searchEndpoint}?q={item_name}");
        lines = (results.text).replace("[", "").replace("]", "").split("\n");

        c = 0
        for line in lines:
            if len(line) < 5: continue;
            info = YoGuide.__parseline(line);

            c+=1

        return found;

    @staticmethod
    def __parseline(self, line: str) -> list:
        return line.replace("(", "").replace(")", "").replace("'", "").split(",");

    @staticmethod
    def change_price(item_id: str, new_price: str) -> bool:
        try:
            check_change = requests.get(f"{API().pricechangeEndpoint}?id={item_id}&price={new_price}")
            if check_change.status_code != 200:
                print("\x1b[31m[x]\x1b[0m Error, Unable to connect to the API (api.yoworld.site)");
                return False
            if "successfully" in check_change.text:
                return True
            return False
        except:
            print("\x1b[31m[x]\x1b[0m Exception Raised On Requests Module....!")
            return False


