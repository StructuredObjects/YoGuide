import requests, json

from .item_search import *

class APIAssets():
    yoworlddb = "https://yoworlddb.com/scripts/getItemInfo.php"; """ POST REQUEST API """
    yoworldinfo = "https://yoworld.info/api/items/"; """ GET REQUEST API """

class ItemGrabber():
    """
        Grabbing item information using Yoworlddb.com API
    """
    @staticmethod
    def GrabItemFromYoworldDB(item_id: str) -> tuple[Item, json.Any]:
        heads = {"Content-Type": "application/x-www-form-urlencoded"};
        id = {"iid": f"{item_id}"}
        item_info = requests.post(APIAssets().yoworlddb, headers=heads, data=id).text;

        json_obj = json.loads(item_info);
        return Item(json_obj['response']['item_name'], json_obj['response']['item_id'], "https://yw-web.yoworld.com/cdn/items/" + json_obj['response']['item_img_bk'], "0", "0"), json_obj;

    @staticmethod
    def GrabItemFromYoworldInfo(item_id: str) -> tuple[Item, json.Any]:
        item_info = requests.get(f"{APIAssets().yoworldinfo}{item_id}").text;
        if item_info.startswith("{") and item_info.endswith("}"): return Item("", "", "", "", "");
    
        json_obj = json.loads(item_info);
        return Item(json_obj['data']['item']['name'], json_obj['data']['item']['id'], "", "0", "0"), json_obj;