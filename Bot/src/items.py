import requests, json

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

class API:
    url = "https://api.yoworld.site"
    searchEndpoint = f"{url}/search"
    advanceEndpoint = f"{url}/advance"
    pricechangeEndpoint = f"{url}/change"

class Item():
    def __init__(self, name = "", iid = 0, url = "", price = "", last_update = "") -> None:
        self.name = name; self.iid = iid; self.url = url;
        self.price = price; self.last_update = last_update;

        if self.price == "0" or self.price == "": self.price = "n/a"
        if self.last_update == "" or self.last_update == "0": self.last_update = "n/a"

        # self.yoworld_price, self.yoworld_update = YoworldItems.getItemPriceFromYwInfo(self.iid)

        
    def arr2item(self, arr: list):
        self.name = arr[0]; self.iid = arr[1]; self.url = arr[2];
        self.price = arr[3]; 
        if len(arr) == 5: self.last_update = arr[4];


class YoworldItems:
    @staticmethod
    def searchItems(item_name: str) -> list:
        found = [];
        results = requests.get(f"{API().searchEndpoint}?q={item_name}");
        lines = (results.text).replace("[", "").replace("]", "").split("\n");

        c = 0
        for line in lines:
            if "src.Items" in line:
                if line.strip().startswith("name: "):
                    i_name = line.strip().replace("name: ", "").replace("'", "");
                    i_id = lines[c+1].strip().replace("id: ", "");
                    i_img = lines[c+2].strip().replace("url: ", "").replace("'", "");
                    i_price = lines[c+3].strip().replace("price: ", "").replace("'", "");
                    i_updated = lines[c+4].strip().replace("last_updated: ", "").replace("'", "");
                    found.append(Item(i_name, i_id, i_img, i_price, i_updated));
            else:
                info = line.split(",");
                if len(info) == 5: found.append(Item(info[0], info[1], info[2], info[3], info[4]));
                else: print(f"An Error Has Occured Trying To Parse An Item....!\n\n{line}")

            c+=1

        return found;

    @staticmethod
    def advanceInfo(item_id: str) -> dict:
        results = requests.get(f"{API().advanceEndpoint}?id={item_id}").text
        results = results.replace("{", "").replace("}", "").replace("'", "").replace("\"", "").replace(", ", "\n");
        
        info = {};
        for line in results.split("\n"):
            if len(line) < 3: break
            args = line.split(":");
            if not "url" in line:
                info[args[0]] = [f"{args[1]}", True]

        return info;


    @staticmethod
    def getItemPriceFromYwInfo(item_id: str) -> tuple[str, str]:
        try:
            item_data = requests.get(f"https://api.yoworld.info/api/items/{item_id}");
            if item_data.status_code != 200:
                print("\x1b[31m[x]\x1b[0m Error, Unable to retrieve item information or connecting to API (api.yoworld.info)");
                return "n/a", "n/a";
            json_data = json.loads(item_data.text)['data']['item']['price_proposals'];
            return f"{json_data[0]}".replace("{", "").replace("}", "").replace("\':\'", ": ").replace("'", "").replace(", ", "\n").split("\n")[6].replace("price: ", "").strip(), f"{json_data[0]}".replace("{", "").replace("}", "").replace("\':\'", ": ").replace("'", "").replace(", ", "\n").split("\n")[2].replace("updated_at: ", "").replace("\"", "").strip();
        except:
            print("\x1b[31m[x]\x1b[0m Error, Unable to retrieve item information or connecting to API (api.yoworld.info)");
            return "n/a", "n/a";

    @staticmethod
    def GrabItemFromYoworldInfo(item_id: str) -> Item:
        print(f"\x1b[31m{item_id}\x1b[0m")
        results = requests.get(f"https://api.yoworld.info/api/items/{item_id}").text;
        if not results.startswith("{") and not results.endswith("}"):
            print(f"[ X ] (INVALID_JSON) Error, Unable to get item information....!\n\n{results}");
            
        
        """ Manually Parsing JSON """
        new = results.replace("\", ", "\n").replace(",\"", "\n").replace("},{", "\n").replace("\":{\"", "\n").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("\":\"", ":").replace("\":", ":").replace("\"", "");
        result_lines = new.split("\n");
        
        info = Item()
        c = 0
        for line in result_lines:
            if "id:" in line and "name:" in result_lines[c+1]:
                info.name = result_lines[c+1].replace("name:", "");
                info.iid = line.replace("id:", "");
                info.url = "";
            
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

            c += 1

        return info;

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


