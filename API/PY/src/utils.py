import os, datetime, enum
from discord_webhook import DiscordWebhook, DiscordEmbed

search_db       = "logs/search.log";
visit_db        = "logs/visit.log";
request_db      = "logs/request.log";
change_db       = "logs/changes.log";

class AppType(enum.Enum):
    DiscordBot      = 0;
    Website         = 1;
    Desktop         = 2;
    All             = 3;

class LogType(enum.Enum):
    Visit           = 0;
    Search          = 1;
    Request         = 2;
    Change          = 3;

class Utils():
    @staticmethod
    def get_date_n_time() -> str:
        return f"{datetime.datetime.now()}".replace(" ", "-").split(".")[0]
    
    @staticmethod
    def parse_line(line: str) -> list:
        return line.replace("(", "").replace(")", "").replace("'", "").split(",");

class Logger():
    @staticmethod
    def NewLog(log: LogType, app: AppType, ipaddr: str, *args: str) -> bool:
        if log == LogType.Visit:
            Logger.LogVisit(Logger.ValidateType(app), ipaddr);
        elif log == LogType.Search:
            if len(args) != 1: return False;
            Logger.LogSearch(Logger.ValidateType(app), ipaddr, args[0]);
        elif log == LogType.Request:
            if len(args) != 2: return False;
            Logger.LogRequest(Logger.ValidateType(app), ipaddr, args[0], args[1]);
        elif log == LogType.Change:
            if len(args) != 5: return False;
            Logger().LogChange(Logger.ValidateType(app), ipaddr, args[0], args[1]);
        
        Logger.send_embed_log(Logger.ValidateType(app), ipaddr, args[0])

        return True;

    @staticmethod
    def send_embed_log(fromApp: str, ipaddr: str, search_query: str) -> None:
        hook = DiscordWebhook("https://discordapp.com/api/webhooks/1105817573842485358/oAxpWtCClWxm8Pl-n9KSESYpXr2t6LoCPZM_Q94DGCoV1TxwiktDWmybC52Ra7c8IgL4")

        embed = DiscordEmbed(title='Price Guide Search Logs', description=f'New Search Logs!', color='ff0000');
        embed.add_embed_field(name='Requested From', value=f'{fromApp}')
        embed.add_embed_field(name='Search Query', value=f'{search_query}')
        embed.add_embed_field(name='User\'s IP', value=f'{ipaddr}')
        embed.set_author(name='Yoworld Price Guide Logs', url='https://images-ext-2.discordapp.net/external/ZZDNlMMvNvguEFDRNa_vTxQEzeEPMUo4xr42dpsoRh4/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1088677293997690961/42a2bc5b79a8c76558eb6b017d9be2e9.png', icon_url='https://images-ext-2.discordapp.net/external/ZZDNlMMvNvguEFDRNa_vTxQEzeEPMUo4xr42dpsoRh4/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1088677293997690961/42a2bc5b79a8c76558eb6b017d9be2e9.png')

        hook.add_embed(embed)
        hook.execute()
        return "GG"

    @staticmethod
    def ValidateType(app: AppType) -> str:
        if app == AppType.DiscordBot:
            return "DISCORD_BOT";
        elif app == AppType.Website:
            return "YOWORLD_SITE";
        elif app == AppType.Desktop:
            return "DESKTOP";

    @staticmethod
    def LogVisit(fromApp: str, ipaddr: str) -> bool:
        if not os.path.exists(visit_db):
            return False;

        file = open(visit_db, "a");
        file.write(f"('{fromApp}','{ipaddr}','{Utils.get_date_n_time()}')\n");
        file.close();
        return True;

    @staticmethod
    def LogSearch(fromApp: str, ipaddr: str, query: str) -> bool:
        if not os.path.exists(search_db):
            return False;
    
        file = open(search_db, "a");
        file.write(f"('{fromApp}','{ipaddr}','{query}','{Utils.get_date_n_time()}')\n");
        file.close();
        return True;

    @staticmethod
    def LogRequest(fromApp: str, ipaddr: str, item_id: str, new_price: str) -> bool:
        if not os.path.exists(request_db):
            return False;

        file = open(request_db, "a");
        file.write(f"('{fromApp}','{ipaddr}','{item_id}','{new_price}','{Utils.get_date_n_time()}')\n");
        file.close();
        return True;

    @staticmethod
    def LogChange(fromApp: str, ipaddr: str, item_id: str, new_price: str) -> bool:
        if not File().Exists(change_db): return False;

        file = open(change_db, "a");
        file.write(f"('{fromApp}','{ipaddr}','{item_id}','{new_price}','{Utils().get_date_n_time()}')\n");
        file.close();
        return True;

class Statistics():
    @staticmethod
    def totalItems() -> int:
        _, line_count = File().Read("items.txt");
        return line_count;

    @staticmethod
    def totalSearches() -> int:
        _, lines_c = File().Read("logs/search.log");
        return lines_c;

    @staticmethod
    def totalAppSearches(app: AppType) -> int:
        app_check = "";

        if app == AppType.Desktop:
            app_check = "DESKTOP";
        elif app == AppType.DiscordBot:
            app_check = "DISCORD_BOT";
        elif app == AppType.Website:
            app_check = "YOWORLD_SITE";

        data, lines = File().Read("log/search.log");
        c = 0;

        for line in data.split("\n"):
            if app == AppType.All:
                if line.startswith(f"('DESKTOP'") | line.startswith(f"('YOWORLD_SITE'") | line.startswith(f"('DISCORD_BOT'"):
                    c += 1;
            elif line.startswith(f"('{app_check}'"):
                c += 1;
        
        return c;

    """
        Return Values: priced_items, no_priced_items, messed_up_items
    """
    @staticmethod
    def totalSortedItems() -> tuple[int, int, int]:
        priced_items, no_priced_items, messed_up_items = 0, 0, 0;
        data, lines = File().Read("items.txt");
        for line in data.split("\n"):
            if len(line)< 5: continue;
            info = Utils().parse_line(line);
            if info[3] == "0" or info[3] == "":
                    no_priced_items += 1;
            elif info[3].endswith("c") or info[3].endswith("k") or info[3].endswith("m") or info[3].endswith("b") or info[3].endswith("yc") or int(info[3].lower().replace("m", "").replace("yc", "").replace("k", "").replace("b", "").replace(".", "").replace("-", "")) > 0:
                    priced_items += 1;
            else:
                    messed_up_items += 1;

        return priced_items, no_priced_items, messed_up_items;



class File():
    @staticmethod
    def Exists(filepath: str) -> bool:
        if not os.path.exists(filepath): return False;
        return True;

    @staticmethod
    def Read(filepath: str):
        if not File().Exists(filepath): return "", 0;
        f = open(filepath, "r"); data = f.read(); f.close();
        return data, len(data.split("\n"));

    @staticmethod
    def Write(filepath: str, new_data: str) -> bool:
        if not File().Exists(filepath): return False;
        f = open(filepath, "w"); f.write(new_data); f.close();
        return True;

    @staticmethod
    def Append(filepath: str, append_data: str) -> bool:
        if not File().Exists(filepath): return False;
        f = open(filepath, "a"); f.write(append_data); f.close();
        return True;
