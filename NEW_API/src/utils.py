import os, enum

class LogDBs:
    search      = "logs/searches.log";
    changes     = "logs/changes.log";
    visits      = "logs/visits.log";
    requests    = "logs/requests.log";

class LogTypes():
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
        current_time = ""
        app = Logger.app2str(appt);
        db = open(Logger.get_db_path(logt), "a");
        if appt == AppType.BOT:
            ## Query
            db.write(f"('{app}','{args[0]}','{current_time}')\n");
        elif appt == AppType.SITE:
            ## Query, IP, Path (Domain Watch)
            db.write(f"('{app}','{args[0]}','{args[1]}','{args[2]}','{current_time}')\n");
        elif appt == AppType.DESKTOP:
            ## Query, IP, PC_INFO
            db.write(f"('{app}','{args[0]}','{args[1]}','{args[2]}','{current_time}')\n");

        db.close();

    @staticmethod
    def app2str(appt: AppType) -> str, str:
        if appt == AppType.BOT:
            return "DISCORDBOT";
        elif appt == AppType.SITE:
            return "SITE";
        elif appt == AppType.DESKTOP:
            return "DESKTOP";

        return "";

    @staticmethod
    def get_db_path(logt: LogTypes) -> str:
        if logt == LogTypes.visits:
            return "logs/visits.log";
        elif logt == LogTypes.searches:
            return "logs/searches";
        elif logt == LogTypes.changes:
            return "logs/changes.log";
        elif logt == LogTypes.requests:
            return "logs/requests.log";

        return "";