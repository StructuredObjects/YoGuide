import requests, json

class Item_Info():
    def __init__(self, n: str, iid: int, u: str, p: str, last_u: str) -> None:
        self.name = n; self.iid = iid; self.url = u;
        self.price = p; self.last_update = last_u;

    def arr2item(self, arr: list):
        self.name = arr[0]; self.iid = arr[1]; self.url = arr[2];
        self.price = arr[3]; self.last_update = arr[4];

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
            "Categorya": self.category,
            "XP": self.xp
        };
        return self.item;

class APIAssets:
    yoworlddb = "https://yoworlddb.com/scripts/getItemInfo.php"; """ POST REQUEST API """
    yoworldinfo = "https://yoworld.info/api/items/"; """ GET REQUEST API """

class ItemGrabber:
    """
        Grabbing item information using Yoworlddb.com API
    """
    @staticmethod
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

    @staticmethod
    def GrabItemPriceFromYwInfo(item_id: str) -> Item_Info:
        results = requests.get(f"https://api.yoworld.info/api/items/{item_id}").text;
        if not results.startswith("{") and not results.endswith("}"):
            print(f"[ X ] (INVALID_JSON) Error, Unable to get item information....!\n\n{results}");
            
        
        """ Manually Parsing JSON """
        new = results.replace("\", ", "\n").replace(",\"", "\n").replace("},{", "\n").replace("\":{\"", "\n").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("\":\"", ":").replace("\":", ":").replace("\"", "");
        result_lines = new.split("\n");

        info = Item_Info("", "", "", "", "");
        c = 0
        for line in result_lines:
            if "id:" in line and "name:" in result_lines[c+1]:
                info.name = result_lines[c+1].replace("name:", "");
                info.iid = line.replace("id:", "");
            
            elif "price:" in line and "approved:" in result_lines[c+1]:
                info.price = line.replace("price:" , ""); ## Replace() to avoid errors
            
            elif "price:" in line and "price_cash:" in result_lines[c+1]:
                if not "approved:" in results:
                    if line.replace("price:", "").strip() != "0":
                        info.price = line.replace("price:", "");
                    elif result_lines[c+1].replace("price_cash:", "").strip() != "0":
                        info.price = result_lines[c+1].replace("price_cash:", "") + "yc";
            
            elif "updated_at:" in line and "deleted_at:" in result_lines[c+1]:
                info.last_update = line.replace("updated_at:", "").replace(" ", "-");
                break

            # elif ""
            c += 1
        info.url = "https://yw-web.yoworld.com/cdn/items/" + info.iid[0:2] + "/" + info.iid[2:4] + "/" + info.iid + "/" + info.iid + "_60_60.gif";
        if info.last_update == "": info.last_update = "0";
        return info;