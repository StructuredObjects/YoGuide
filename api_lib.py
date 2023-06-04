import requests, enum

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

class Response(enum.Enum):
    NONE    = 0
    EXACT   = 1
    EXTRA   = 2

class YoworldEngine():
    items: list[Item];
    found: list[Item];

    def __init__(self):
        self.__retriveItems();

    def updateDB(self) -> None:
        self.__retriveItems();
    
    def Search(self, q: str) -> Response:
        self.query = q;
        if q.isdigit() or isinstance(q, int):
            self.found = [self.__searchByID()];
            return Response.EXACT;

        self.__searchByName();
    
        if len(self.found) > 1:
            return Response.EXTRA;
        elif len(self.found) == 1:
            return Response.EXACT;

        return Response.NONE;

    def getResults(self) -> list[Item]:
        return self.found;

    def __retriveItems(self) -> None:
        self.items = [];
        db = open("items.txt", "r");
        lines = db.read().split("\n");

        """
            LINE FORMAT:
            ('item_name','item_id','item_imgurl','item_price','item_update')
        """
        for line in lines:
            if len(line) < 5: continue;
            info = YoworldEngine.parseLine(line);
            if len(info) == 5:
                self.items.append(YoworldEngine.newItem(info));
    
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

        return Item();


    @staticmethod
    def parseLine(line: str) -> list:
        return line.replace("(", "").replace(")", "").replace("'", "").split(",");

    @staticmethod
    def newItem(arr: list) -> Item:
        itm = Item();
        itm.name = arr[0]; itm.id = int(arr[1]); itm.url = arr[2]; 
        itm.price = arr[3]; itm.update = arr[4];

        if "yc" in arr[3]:
            yc = arr[3].replace("yc", "").replace("/", "").replace(" ", "");
            conv_coins = int(yc)*60000;
            itm.price = f"{arr[3]}/{conv_coins}c";
        
        return itm;
