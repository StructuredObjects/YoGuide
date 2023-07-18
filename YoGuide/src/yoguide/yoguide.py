import requests, enum, datetime, requests, json

db_path = "items.txt";

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
    category:       str;
    


class Response(enum.Enum):
    NONE    = 0;
    EXACT   = 1;
    EXTRA   = 2;

class YoGuide():
    items: list[Item];
    found: list[Item];

    def __init__(self):
        self.__retriveItems();
    
    def Search(self, q: str) -> Response:
        self.query = q;
        if q.isdigit() or isinstance(q, int):
            """
                Search for item ID in our database
            """
            self.found = [self.__searchByID()];
            if self.found[0].name != "":
                return Response.EXACT;

            """
                Search item ID using YoworldDB.com and Yoworld.info API
                as an alternative route and//or missing the searched item in our database
            """
            n = YoGuide.newItem(["", f"{q}", "", "", ""])
            ywdb_item = ItemSearch.ywdbSearch(n, True, q);
            ItemSearch.ywinfoSearch(n);

            YoGuide.add_new_item(ywdb_item)
            self.found = [n];
            if self.found[0].name != "":
                return Response.EXACT;

        """
            Search for item name in our database!
        """
        self.__searchByName();
    
        if len(self.found) > 1:
            return Response.EXTRA;
        elif len(self.found) == 1:
            if self.found[0].name != "":
                return Response.EXACT;

        return Response.NONE;

    def getResults(self, rtype: Response) -> list[Item] | Item:
        if rtype == Response.NONE: return [YoGuide.newItem(["", "0", "", "", ""])];
        if rtype == Response.EXACT: return self.found[0];
        return self.found;

    def __retriveItems(self) -> None:
        self.items = [];
        db = open(db_path, "r");
        lines = db.read().split("\n");

        """
            LINE FORMAT:
            ('item_name','item_id','item_imgurl','item_price','item_update')
        """
        for line in lines:
            if len(line) < 5: continue;
            info = YoGuide.parseLine(line);
            if len(info) == 5:
                self.items.append(YoGuide.newItem(info));
    
    def __searchByName(self) -> list[Item]:
        self.found = []
        for item in self.items:
            no_case_sen = self.query.lower();

            if item.name == self.query: 
                return [item];

            if self.query in item.name or no_case_sen in item.name.lower():
                self.found.append(item);
                continue;

            if " " in self.query:
                words = no_case_sen.split(" ")
                matchh = 0;
                for word in words:
                    if word in item.name:
                        matchh += 1;

                        if matchh > 1:
                            self.found.append(item);
                            continue;
        return self.found
    
    def __searchByID(self) -> Item:
        for item in self.items:
            if f"{item.id}" == f"{self.query}":
                return item;

        return YoGuide.newItem(["", "0", "", "", ""]);

    @staticmethod
    def changePrice(itm: Item, n_price: str) -> bool:
        r = False;
        db = open(db_path, "r");

        lines = db.read().split("\n");

        new_db = "";
        new_update = f"{datetime.datetime.now()}".split(".")[0].replace(" ", "-");

        for line in lines:
            if len(line) < 5: continue;
            info = YoGuide.parseLine(line)
            item_info = YoGuide.newItem(YoGuide.parseLine(line));
            if len(info) == 5:
                if item_info.id == itm.id:
                    new_db += f"('{itm.name}','{itm.id}','{itm.url}','{n_price}','{new_update}')\n";
                    r = True;
                else:
                    new_db += f"{line}\n";
        
        db.close();

        newdb = open(db_path, "w");
        newdb.write(new_db);
        newdb.close();

        return r;

    @staticmethod
    def add_new_item(item: Item) -> bool:
        db = open(db_path, "a");
        db.write(f"('{item.name}','{item.id}','{item.url}','0','0')\n");
        db.close()
        return True;
    
    @staticmethod
    def isID(q: str) -> bool:
        if q.isdigit() or isinstance(q, int):
            return True;
        return False;

    @staticmethod
    def parseLine(line: str) -> list:
        return line.replace("(", "").replace(")", "").replace("'", "").split(",");

    @staticmethod
    def newItem(arr: list[str]) -> Item:
        itm = Item();
        itm.name = arr[0]; itm.id = int(arr[1]); itm.url = arr[2]; 
        itm.price = arr[3]; itm.update = arr[4];

        if arr[3].endswith("yc"):
            yc = arr[3].replace("yc", "").replace("/", "").replace(" ", "").lower().replace("in-store", "");
            conv_coins = int(yc)*60000;
            itm.price = f"{arr[3]}/{conv_coins}c";

        if itm.price == "" or itm.price == "0": 
            itm.price = "N/A";
            itm.update = "N/A";
        
        return itm;

    @staticmethod
    def item2dict(itm: Item) -> dict:
        return {"Name": itm.name,
                    "ID": itm.id,
                    "Price": itm.price,
                    "Update": itm.update};

    @staticmethod
    def addInfo(itm: Item, j: dict) -> dict:
        j['Tradable'] = itm.is_tradable;
        j['Giftable'] = itm.is_giftable;
        j['In Store'] = itm.in_store;
        j['Store Price'] = itm.store_price;
        j['Gender'] = itm.gender;
        j['XP'] = itm.xp;
        j['Category'] = itm.category;

        return j;


class ItemSearch:
    @staticmethod
    def ywdbSearch(item: Item, add_main_info: bool = False, iid: str = "") -> None:
        heads = {"Content-Type": "application/x-www-form-urlencoded"};

        if iid != "": id = {"iid": f"{iid}"};
        else: id = {"iid": f"{item.id}"};
        
        results = requests.post("https://yoworlddb.com/scripts/getItemInfo.php", headers=heads, data=id).text;

        if not results.startswith("{") or not results.endswith("}"):
            print(f"[ X ] (INVALID_JSON) Error, Unable to get item information....!\n\n{results}");
            return;

        info = json.loads(results)['response'];

        if add_main_info:
            item.name = info['item_name'];
            n = str(iid)
            if item.id: n = str(item.id);
            item.url = f"https://yw-web.yoworld.com/cdn/items/{n[:2]}/{n[2:4]}/{n}/{n}_60_60.gif"

        item.gender = info['gender'];
        item.is_tradable = info['is_tradable'];
        item.is_giftable = info['can_gift'];
        item.category = info['category'];
        item.xp = info['xp'];

        if info['active_in_store'] == "1": item.in_store = True;
        else: item.in_store = False;

        if info['price_coins'] != "0": item.store_price = f"{info['price_coins']}c";
        elif info['price_cash'] != "0": item.store_price = f"{info['price_cash']}yc"
        else: item.store_price = "0";
        
        return item;

    @staticmethod
    def ywinfoSearch(item: Item, add_main_info: bool = False) -> bool:
        req = requests.get(f"https://api.yoworld.info/api/items/{item.id}");
        if req.status_code != 200:
            print("[ X ] Error, Unable to connect to 'api.yoworld.info'....!");
            return False;

        results = req.text;

        obj = json.loads(results);
        obj['data']['item']['price_proposals'];

        lines = f"{obj}".replace(", ", "\n").replace("'", "").replace("\"", "").replace(", ", "").replace("{", "").replace("}", "").split("\n");

        history = {};
        
        search = False;
        time = "";
        price = "";
        approved = "";

        for line in lines:
            if "price_proposals" in line:
                search = True;

            if search:
                if "updated_at: " in line:
                    time = line.replace("updated_at: ", "");
                
                if "price: " in line:
                    price = line.replace("price: ", "");

                if "username: " in line:
                    approved = line.replace("username: ", "");
                    history[price] = f"{time}//{approved}";

        return True;