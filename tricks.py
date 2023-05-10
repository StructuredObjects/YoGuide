import os, sys, time, requests, json

heads = {"Content-Type": "application/x-www-form-urlencoded"};
id = {"iid": f"257460"};
results = requests.post("https://yoworlddb.com/scripts/getItemInfo.php", headers=heads, data=id).text;


if not results.startswith("{") or not results.endswith("}"):
    print(f"[ X ] (INVALID_JSON) Error, Unable to get item information....!\n\n{results}");
    exit(0);

json_obj = json.loads(results)['response']['item_img'];

print(json_obj);