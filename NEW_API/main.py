import logging, requests

from flask                  import Flask, request
from src.yoguide.yoguide    import *

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True


@app.route('/')
def index():
    return 'Welcome To Yoworld.site API v2.0 (Flask Python Version)'

@app.route('/stats')
def statistics():
    return "";

"""
    Search Engine
"""
@app.route('/search')
def search():
    search = request.args.get('q');
    # ip = request.environ['HTTP_CF_CONNECTING_IP'];

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

@app.route("/advance")
def advance_search():
    query = request.args.get('id');
    return ""

        

"""
    Price Change
"""
@app.route("/change")
def change():
    i_id = request.args.get('id');
    n_price = request.args.get('price');
    ip = request.environ['HTTP_CF_CONNECTING_IP'];

"""
    Request Price Change
"""
@app.route("/request")
def request_change():
    item_name = request.args.get('name')
    item_id = request.args.get('id');
    price_req = request.args.get('price');
    return ""

@app.route("/app")
def appNews():
    return f"defdfds";

@app.route("/ip")
def get_client_ip():
    ip = request.environ['HTTP_CF_CONNECTING_IP']
    return f"IP: {ip}"
    
if __name__ == '__main__':
    ip = requests.get("https://api.ipify.org").text
    app.run(host="127.0.0.1", port=80)