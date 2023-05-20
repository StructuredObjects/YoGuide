import requests, enum, json

class API:
    url                 = "https://api.yoworld.site"
    searchEndpoint      = f"{url}/search"
    infoEndpoint        = f"{url}/advance"
    changeEndpoint      = f"{url}/change"
    statsEndpoint       = f"{url}/stats"

class Results(enum.Enum):
    NONE                = 0
    EXACT_FOUND         = 1
    EXTRA_FOUND         = 2

class Item():
    """ Main Item Information Needed """
    name: str
    id: int
    url: str
    price: str
    update: str

    """ Extra Item Information """
    gender: str
    is_free_gift: bool
    is_tradable: bool
    is_giftable: bool
    is_instore: bool
    category: str
    xp: int
    def __init__(self) -> None:
        pass

    def new_item(self, n: str, iid: int, u: str, p: str, last_u: str) -> None:
        self.name = n; self.id = iid; self.url = u;
        self.price = p; self.last_update = last_u;

    def arr2item(self, arr: list) -> None:
        if len(arr) != 5:
            print(f"[ X ] Error, Unable to parse this list ( {arr} )");
            return;
    
        self.name = arr[0]; 
        self.id = arr[1]; 
        self.url = arr[2];
        self.price = arr[3]; 
        self.last_update = arr[4];

    def add_extra_info(self, arr: list) -> None:
        if len(arr) != 7:
            print(f"[ X ] Error, Unable to parse this list ( {arr} )");
            return;
    
        self.gender = arr[0];
        self.is_tradable = bool(int(arr[1]));
        self.is_free_gift = bool(int(arr[2]));
        self.is_giftable = bool(int(arr[3]));
        self.is_instore = bool(int(arr[4]))
        self.category = arr[5];
        self.xp = arr[6];

class YoworldSite:
    @staticmethod
    def ResultCheck(results: list) -> Results:
        if results == []: return Results.NONE;
        elif results == ['']: return Results.NONE;
        elif results == 1: return Results.EXACT_FOUND;
        elif results > 1: return Results.EXTRA_FOUND;

    @staticmethod 
    def searchItem(query: str) -> list:
        if len(query) == 0: return [];
        results = requests.get(f"{API.searchEndpoint}?q={query}")
        if results.status_code != 200:
            return []; ## RETURN NOTHING IF API IS DOWN

        response = results.text;

        if response == "[ X ] Error, You must fill all parameters to continue!": return [];
        if "No items found" in response: return [];
        if "\n" not in response: return [response]; ## DETECTED ONLY ONE ITEM! RETURN IT
        
        lines = response.split("\n");
        found = [];

        for line in lines:
            if len(line) < 5: break;
            info = line.replace("[", "").replace("]", "").split(",");
            if len(info) == 5:
                new_item = Item("", "", "", "", "");
                new_item.arr2item(info)
                found.append(new_item);
            else:
                print(f"[ X ] Error, Unable to parse this line!\n{line}");

        return found;

    @staticmethod
    def infoSearch(item_id: int, itm: Item | None) -> Item:
        if len(item_id) == 0: return Item("", "", "", "", "");
        result = requests.get(f"{API().infoEndpoint}?q={item_id}");
        if result.status_code != 200:
            print("[ X ] Error, API is down...!");
            return Item("", "", "", "", "");

        response = result.text;

        if not response.startswith("{") and not response.endswith("}"): return Item("", "", "", "", "");
        if response == "[x] Error, Invalid Item ID.....!": return Item("", "", "", "", "");

        json_obj = json.loads(response)
        item_info = [];
        for key in json_obj:
            val = json_obj[key]
            item_info.append(val)

        if itm != None:
            itm.add_extra_info(item_info);
            return itm;

        new_item = Item();
        new_item.add_extra_info(item_info);
        return new_item;

    @staticmethod
    def priceChange(item_id: int, price: int) -> bool:
        if len(item_id) == 0: return Item("", "", "", "", "");
        results = requests.get(f"{API().changeEndpoint}?id={item_id}&price={price}");
        if results.status_code != 200:
            print("[ X ] Error, API is down...!");
            return False;

        response = results.text;

        if response == "No Item found to update...!": return False;
        if response == "Unable to update item!": return False;
        if response.strip().endswith("successfully updated!"): return True;
        return False;

    @staticmethod
    def stats() -> list[int]:
        results = requests.get(f"{API().statsEndpoint}")
        if results.status_code != 200:
            return 0, 0, 0;
    
        response = results.text;

        if not "," in response:
            return 0, 0, 0;

        return response.split(",");