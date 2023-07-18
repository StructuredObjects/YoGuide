import sys

from src.logger import *
from src.yoguide.yoguide import *

args = sys.argv;

if len(args) < 2:
    print(f"[ X ] Error, Invalid argument provided\nUsage: {args[0]} <query>");
    exit(0);

query = f"{args}".replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace(f"{args[0]} ", "").replace(f"{args[0]}", "");

eng = YoGuide()
n = eng.Search(query);

Logger.newLog(AppType.DESKTOP, LogTypes.SEARCH, query, "1.1.1.1");

if n == Response.NONE:
    print("[ X ] Unable to find item.....!");
    exit(0);

elif n == Response.EXACT:

    r = eng.getResults(n);
    gg = ItemSearch.ywdbSearch(r);
    nn = ItemSearch.ywinfoSearch(r)
    print(f"Item: {r.name} | {r.id} | {r.price} | {r.update} | {r.is_tradable}");
    exit(0);

elif n == Response.EXTRA:
    r = eng.getResults();
    c = 0;
    for itm in r:
        print(f"Item: {r[c].name} | {r[c].id} | {r[c].price} | {r[c].update}");
        c += 1