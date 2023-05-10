import requests, json

class Item_Info():
    def __init__(self, n: str, iid: int, u: str, p: str, last_u: str) -> None:
        self.name = n; self.iid = iid; self.url = u;
        self.price = p; self.last_update = last_u;

    def arr2item(self, arr: list):
        self.name = arr[0]; self.iid = arr[1]; self.url = arr[2];
        self.price = arr[3]; self.last_update = arr[4];

class APIAssets:
    yoworlddb = "https://yoworlddb.com/scripts/getItemInfo.php"; """ POST REQUEST API """
    yoworldinfo = "https://yoworld.info/api/items/"; """ GET REQUEST API """

class ItemGrabber:
    """
        Grabbing item information using Yoworlddb.com API
    """
    @staticmethod
    def GrabItemFromYoworldDB(item_id: str) -> str:
        heads = {"Content-Type": "application/x-www-form-urlencoded"};
        id = {"iid": f"257460"};
        results = requests.post("https://yoworlddb.com/scripts/getItemInfo.php", headers=heads, data=id).text;


        if not results.startswith("{") or not results.endswith("}"):
            print(f"[ X ] (INVALID_JSON) Error, Unable to get item information....!\n\n{results}");
            return;

        return json.loads(results)['response']['item_img'];

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