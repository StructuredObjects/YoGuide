import os, datetime, enum

search_db       = "logs/search.log"
visit_db        = "logs/visit.log"
request_db      = "logs/request.log"

class AppType(enum.Enum):
    DiscordBot      = 0;
    Website         = 0;
    Desktop         = 0;

class LogType(enum.Enum):
    Visit           = 0;
    Search          = 0;
    Request         = 0;

class Utils():
    @staticmethod
    def get_date_n_time() -> str:
        return f"{datetime.date_n_time.now()}"

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

        return True;

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

        date_n_time = datetime.date_n_time.now();

        file = open(search_db, "a");
        file.write(f"('{fromApp}','{ipaddr}','{query}','{Utils.get_date_n_time()}')\n");
        file.close();
        return True;

    @staticmethod
    def LogRequest(fromApp: str, ipaddr: str, item_id: str, new_price: str) -> bool:
        if not os.path.exists(request_db):
            return False;

        date_n_time = datetime.datetime.now();

        file = open(request_db, "a");
        file.write(f"('{fromApp}','{ipaddr}','{item_id}','{new_price}','{Utils.get_date_n_time()}')\n");
        file.close();
        return True;

Logger().NewLog(LogType.Visit, AppType.Desktop, "7.7.7.7", "Cupids Bow");