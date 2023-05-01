import requests, json

class API:
    url = "https://api.yoworld.site"
    searchEndpoint = f"{url}/search"
    pricechangeEndpoint = f"{url}/change"

class Item():
    def __init__(self, name = "", iid = 0, url = "", price = "", last_update = "") -> None:
        self.name = name; self.iid = iid; self.url = url;
        self.price = price; self.last_update = last_update;

        if self.price == "0" or self.price == "": self.price = "n/a"
        if self.last_update == "" or self.last_update == "0": self.last_update = "n/a"

        self.yoworld_price, self.yoworld_update = YoworldItems.getItemPriceFromYwInfo(self.iid)

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


