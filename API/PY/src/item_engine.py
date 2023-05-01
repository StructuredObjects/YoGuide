import os, requests, datetime

class Item():
    def __init__(self, n: str, iid: int, u: str, p: str, last_u: str) -> None:
        self.name = n; self.iid = iid; self.url = u;
        self.price = p; self.last_update = last_u;

class YoworldItems():
    data = ""
    def __init__(self) -> None:
        self.__fetchItem();

    def __parseline(self, line: str) -> list:
        return line.replace("(", "").replace(")", "").replace("'", "").split(",");

    def __fetchItem(self) -> None:
        self.items = []
        
        file = open("items.txt", "r");
        self.data = file.read()
        lines = self.data.split("\n");

        for line in lines:
            if len(line) < 5: continue;
            info = self.__parseline(line);
            self.items.append(Item(info[0], int(info[1]), info[2], info[3], info[4]));
        
        file.close()
            

    def new_search(self, s) -> list:
        self.search = s;
        if s.isdigit():
            return [self.searchByID()];
        return self.searchByName();

    def searchByName(self) -> list:
        self.found = []
        for item in self.items:
            no_case_sen = self.search.lower();

            if item.name == self.search: 
                return [item];

            if self.search in item.name or no_case_sen in item.name:
                self.found.append(item);

            if " " in self.search:
                words = no_case_sen.split(" ")
                if len(words) < 2:
                    for word in words:
                        if word in item.name:
                            self.found.append(item);
                else:
                    matchh = 0;
                    for word in words:
                        if word in item.name:
                            matchh += 1;

                            if matchh > 1:
                                self.found.append(item);
        return self.found
                        
    def searchByID(self) -> Item:
        for item in self.items:
            if f"{item.iid}" == f"{self.search}": return item;

        return Item("", "", "", "", "")

    def change_price(self, item_id: str, new_price: str) -> bool:
        items = ""
        found = False
        time = datetime.datetime.now()
        time = f"{time}".split(".")[0].replace(" ", "-")
        for i in self.items:
            if f"{i.iid}" == f"{item_id}":
                items += f"('{i.name}','{i.iid}','{i.url}','{new_price}','{time}')\n"
                found = True
            else:
                items += f"('{i.name}','{i.iid}','{i.url}','{i.price}','{i.last_update}')\n"

        new_db = open("items.txt", "w")
        new_db.write(items)
        new_db.close()
        return found