import os

class User():
    name:           str;
    user_id:        int;
    changes:        int;
    changes_w:      int;
    
    def __init__(self, arr: list[str]):
        self.user = arr[0]; self.user_id = arr[1];
        self.changes = arr[2]; self.changes_w = arr[3];

class Crud():
    users:  list[User];
    def __init__(self):
        self.__parseUsers();
    
    def __parseLine(self, line: str) -> list[str]:
        return line.split("(", "").replace(")", "").replace("'", "").split(",");

    def __parseUsers(self) -> None:
        self.users = [];
        db = open("assets/users.db", "r");
        
        lines = db.read().split("\n");

        for line in lines:
            if len(line) < 2: continue;
            info = self.__parseLine(line);
            if info == 4:
                self.users.append(User(info));
            else:
                print("[ X ] Error, Unable to parse user....!");

    def searchUser(self, user_id: str) -> User:
        self.users = [];
        for user in self.users:
            if f"{user.user_id}" == f"{user_id}":
                return user;
    
        return User(["", "", "", ""]);

    def updateUser(self, u: User, total_count: str, new_count: str) -> bool:
        new_db = ""; file = open("assets/users.db", "w"); user_found = False;
        
        for user in self.users:
            if f"{user.user_id}" == f"{u.user_id}":
                new_db = f"('{user.name}','{user.user_id}','{total_count}','{new_count}')\n";
                user_found = True
            else:
                new_db = f"('{user.name}','{user.user_id}','{user.changes}','{user.changes_w}')\n";

        file.write(new_db);
        file.close();
        return user_found;


    def removeUser(self, u: User) -> bool:
        new_db = ""; file = open("assets/users.db", "w");

        for user in self.users:
            if f"{user.user_id}" != f"{u.user_id}":
                new_db = f"('{user.name}','{user.user_id}','{user.changes}','{user.changes_w}')\n";

        file.write(new_db);
        file.close(); 
        return True;