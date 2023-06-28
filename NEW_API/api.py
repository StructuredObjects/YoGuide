import logging, requests

from flask                       import Flask, request
from src.logger                  import *
from src.yoguide.yoguide         import *
from src.yoguide.item_searches   import *

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True


@app.route('/')
def index():
    return 'Welcome To Yoworld.site API v2.0 (Flask Python Version)'

"""
    Search Engine
"""
@app.route('/search')
def search():
    search = request.args.get('q');
    ip = "1.1.1.1";
    
    if "HTTP_CF_CONNECTING_IP" in request.environ:
        ip = request.environ['HTTP_CF_CONNECTING_IP'];

    if search == "" or len(search) < 2: return ""; 

    """
        Search Engine Using YoGuide Lib
    """
    eng = YoGuide()
    n = eng.Search(search);

    if n == Response.NONE:
        return "[ X ] Unable to find item.....!";

    if ip == "66.45.249.155":
        Logger.newLog(AppType.BOT, LogTypes.SEARCH, search, ip);
    elif ip == "216.219.86.171":
        Logger.newLog(AppType.SITE, LogTypes.SEARCH, search, ip);
    else:
        Logger.newLog(AppType.DESKTOP, LogTypes.SEARCH, search, ip);

    if n == Response.EXACT:
        r = eng.getResults(n);
        try:
            ItemSearch.ywdbSearch(r);
            ItemSearch.ywinfoSearch(r);
            return f"[{r.name},{r.id},{r.url},{r.price},{r.update},{r.is_tradable},{r.is_giftable},{r.in_store},{r.store_price},{r.gender},{r.xp},{r.category}]";
        except Exception as e:
            print(f"[ X ] Unable to get extra info {e}...");
            return f"[{r.name},{r.id},{r.url},{r.price},{r.update}]";

    elif n == Response.EXTRA:
        r = eng.getResults(n);
        c = 0; n = "";
        for itm in r:
            try:
                ItemSearches.ywdbSearch(itm);
                ItemSearches.ywinfoSearch(itm);
                if c == len(r): n += f"[{itm.name},{itm.id},{itm.url},{itm.price},{itm.update},{itm.is_tradable},{itm.is_giftable},{itm.in_store},{itm.store_price},{itm.gender},{itm.xp},{itm.category}]";
                else: n += f"[{itm.name},{itm.id},{itm.url},{itm.price},{itm.update},{itm.is_tradable},{itm.is_giftable},{itm.in_store},{itm.store_price},{itm.gender},{itm.xp},{itm.category}]\n";
            except: 
                print("[ x ] Error, Unable to catch other infoamtion for this item...!");
                if c == len(r): n += f"[{itm.name},{itm.id},{itm.url},{itm.price},{itm.update}]";
                else: n += f"[{itm.name},{itm.id},{itm.url},{itm.price},{itm.update}]\n";
            c += 1;

        return f"{n}"
    return "";    
  
if __name__ == '__main__':
    ip = requests.get("https://api.ipify.org").text
    app.run(host=ip, port=80)