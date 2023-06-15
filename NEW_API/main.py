import logging, requests

from flask                  import Flask, request
from src.yoguide.yoguide    import *

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

    if search == "" | len(search) < 2: return ""; 

    """
        Search Engine Using YoGuide Lib
    """
    eng = YoworldEngine()
    n = eng.Search(search);

    if n == Response.NONE:
        return "[ X ] Unable to find item.....!";

    elif n == Response.EXACT:
        r = eng.getResults();
        return f"[{r[0].name},{r[0].id},{r[0].price},{r[0].update}]";

    elif n == Response.EXTRA:
        r = eng.getResults();
        c = 0; n = "";
        for itm in r:
            try:
                ItemSearches.ywdbSearch(itm);
                ItemSearches.ywinfoSearch(itm);
            except: print("[ x ] Error, Unable to catch other infoamtion for this item...!")
            if c == len(r): n += f"[{itm.name},{itm.id},{itm.url},{itm.price},{itm.update}]";
            else: n += f"[{itm.name},{itm.id},{itm.url},{itm.price},{itm.update}]\n";
            c += 1

        return f"{n}"
    return "";    
  
if __name__ == '__main__':
    ip = requests.get("https://api.ipify.org").text
    app.run(host="127.0.0.1", port=80)