import os, sys, time, requests, json

class YWDB_Item():
        iid: str
        name: str
        gender: int
        price_coins: int
        price_cash: int
        is_tradable: int
        is_free_gift: int
        can_gift: int
        in_store: int
        image_url: str
        category: str
        xp: int
        def __init__(self, info: list):
            if len(info) == 15: return;
            self.iid = int(info[0]);
            self.name = info[1];
            self.gender = int(info[2]);
            self.price_coins = int(info[3]);
            self.price_cash = int(info[4]);
            self.is_tradable = int(info[5]);
            self.is_free_gift = int(info[6]);
            self.can_gift = int(info[7]);
            self.in_store = int(info[8]);
            self.image_url = info[9];
            self.category = info[10];
            self.xp = int(info[11]);

        def item2dict(self) -> dict:
            self.item = {
                  "ID": self.iid,
                  "Name": self.name,
                  "Gender": self.gender,
                  "Price Coins": self.price_coins,
                  "Price Cash": self.price_cash,
                  "Tradable": self.is_tradable,
                  "Free Gift": self.is_free_gift,
                  "Giftable": self.can_gift,
                  "In-Store": self.in_store,
                  "ImgURL": self.image_url,
                  "Category": self.category,
                  "XP": self.xp
            };

            return self.item;
API_URL = "";

def GrabItemFromYoworldDB(item_id: str) -> YWDB_Item:
        heads = {"Content-Type": "application/x-www-form-urlencoded"};
        id = {"iid": f"{item_id}"};
        results = requests.post("https://yoworlddb.com/scripts/getItemInfo.php", headers=heads, data=id).text;

        if not results.startswith("{") or not results.endswith("}"):
            print(f"[ X ] (INVALID_JSON) Error, Unable to get item information....!\n\n{results}");
            return;

        info = json.loads(results)['response'];
        keys = ['id', 'item_name', 'gender', 'price_coins', 'price_cash', 'is_tradable', 'is_free_gift', 'can_gift', 'active_in_store', 'item_img_bk', 'category', 'xp'];
        values = [];

        for key in info:
              value = info[key];
              if key in keys: values.append(value);
        
        return YWDB_Item(values);

itm = GrabItemFromYoworldDB("26295");
print(f"{itm.item2dict()}".replace(",", "\n"))