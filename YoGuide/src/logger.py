import os, enum, datetime

from .user_crud import *

class LogDBs:
    search      = "logs/searches.log";
    changes     = "logs/changes.log";
    visits      = "logs/visits.log";
    requests    = "logs/requests.log";

class LogTypes(enum.Enum):
    NONE        = 0;
    VISIT       = 1;
    SEARCH      = 2;
    CHANGE      = 3;
    REQUEST     = 4;

class AppType(enum.Enum):
    NONE        = 0;
    BOT         = 1;
    SITE        = 2;
    DESKTOP     = 3;

class Logger():
    """
        Logging all actions within the application 
        with user's IP Address
    """
    @staticmethod
    def newLog(appt: AppType, logt: LogTypes, *args) -> None:
        if len(args) < 1: return;
        
        current_time = f"{datetime.datetime.now()}".split(".")[0].replace(" ", "-");
        app = Logger.app2str(appt);
        db = open(Logger.get_db_path(logt), "a");

        if appt == AppType.BOT:
            """
                ('DISCORDBOT','USER_ID','QUERY','RESULTTYPE','FOUND_COUNT','CURRENTTIME')
                                   0       1          2            3
            """
            db.write(f"('{app}','{args[0]}','{args[1]}','{args[2]}','{args[3]}','{current_time}')\n");
        elif appt == AppType.SITE:

            """
                ('SITE','IP_ADDR','QUERY','RESULTTYPE','FOUND_COUNT','CURRENTTIME')
            """
            db.write(f"('{app}','{args[0]}','{args[1]}','{args[2]}','{current_time}')\n");
        elif appt == AppType.DESKTOP:
            ## Query, IP, PC_INFO
            db.write(f"('{app}','{args[0]}','{args[1]}','{current_time}')\n");

        db.close();

    @staticmethod
    def app2str(appt: AppType) -> str:
        if appt == AppType.BOT:
            return "DISCORDBOT";
        elif appt == AppType.SITE:
            return "SITE";
        elif appt == AppType.DESKTOP:
            return "DESKTOP";

        return "";

    @staticmethod
    def get_db_path(logt: LogTypes) -> str:
        if logt == LogTypes.VISIT:
            return LogDBs.visits;
        elif logt == LogTypes.SEARCH:
            return LogDBs.search;
        elif logt == LogTypes.CHANGE:
            return LogDBs.changes;
        elif logt == LogTypes.REQUEST:
            return LogDBs.requests;

        return "";
