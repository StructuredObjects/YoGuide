import logging, requests

from flask                       import Flask, request
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
    # ip = request.environ['HTTP_CF_CONNECTING_IP'];

    if search == "" or len(search) < 2: return ""; 

    """
        Search Engine Using YoGuide Lib
    """
    eng = YoworldEngine()
    n = eng.Search(search);

    if n == Response.NONE:
        return "[ X ] Unable to find item.....!";

    elif n == Response.EXACT:
        r = eng.getResults();
        try:
            ItemSearch.ywdbSearch(r[0]);
            ItemSearch.ywinfoSearch(r[0]);
            return f"[{r[0].name},{r[0].id},{r[0].url},{r[0].price},{r[0].update},{r[0].is_tradable},{r[0].is_giftable},{r[0].in_store},{r[0].store_price},{r[0].gender},{r[0].xp},{r[0].category}]";
        except Exception as e:
            print(f"[ X ] Unable to get extra info {e}...");
            return f"[{r[0].name},{r[0].id},{r[0].url},{r[0].price},{r[0].update}]";

    elif n == Response.EXTRA:
        r = eng.getResults();
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