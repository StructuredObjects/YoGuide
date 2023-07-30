module yg

import x.json2 as jsn
import net.http as web

pub fn retrieve_item_info(mut Item itm, bool add_main) Item
{
	data := {'id': itm.id}
	resp := web.post_form("https://yoworlddb.com/scripts/getItemInfo.php", data)

	if resp.starts_with("{") == false && resp.ends_with("}") == false {
		println("[ X ] Warning, Unable to get the correct response from 'api.yoworld.info'....!")
		return itm
	}

	jsn_obj 	:= (jsn.raw_decode(resp) or { 0 }).as_map()
	resp_obj 	:= (jsn.raw_decode("${jsn_obj}") or { return itm }).as_map()
	
	itm.gender 			= resp_obj['gender'] or { "" }
	itm.is_tradable 	= resp_obj['is_tradable'] or { "" }
	itm.is_giftable 	= resp_obj['can_gift'] or { "" }
	itm.category 		= resp_obj['category'] or { "" }
	itm.xp 				= resp_obj['xp'] or { "" }

	in_store := jsn_obj['active_in_store'] or { "" }
	if in_store { itm.in_store == true } else { itm.in_store = true }

	price_coins 	:= jsn_obj['price_coins']
	price_cash 		:= jsn_obj['price_cash']

	if add_main
	{
		itm.name 	= jsn_obj['item_name'] or { "" }
		itm.id 		= jsn_obj['id'] or { "" }
		itm.url 	= "https://yw-web.yoworld.com/cdn/items/${n[..2]}/${n[2..4]}/${n}/${n}_60_60.gif"
		
		if price_coins.int() > 0 {
			itm.yw_db_price = "${price_coins}c"
		} else if price_cash.int() > 0 {
			itm.yw_db_price = "${price_cash}yc"
		}
	}

	return itm
}

pub fn retrieve_item_ywinfo_price(mut Item itm, bool add_main) Item
{
	resp = web.get_text("https://api.yoworld.info/api/items/${itm.id}")

	if resp.starts_with("{") == false && resp.ends_with("}") == false
	{ return itm }

	jsn_obj 	:= (jsn.raw_decode(resp) or { return itm }).as_map()
	data 		:= (jsn.raw_decode("${jsn_obj['data']}") or { return itm }).as_map()
	item_data	:= (jsn.raw_decode("${data['item']}") or { return itm }).as_map()
	price_prop	:= (jsn.raw_decode("${item_data['price_proposal']}") or { return itm }).as_map()
	
    mut search 		= false;
    mut time 		= "";
    mut price 		= "";
    mut approved 	= "";

    for line in lines
	{
        if "price_proposals" in line {
            search = true 
		}

        if search {
            if "updated_at: " in line {
                time = line.replace("updated_at: ", "")
			}
            
            if "price: " in line {
                price = line.replace("price: ", "")
			}
				
            if "username: " in line {
                approved = line.replace("username: ", "")
                history[price] = f"{time}//{approved}"
			}
		}
	}

	itm.yw_info_price 		= price
	itm.yw_info_update 		= update
	itm.yw_info_approval 	= approved

	if add_main {
		itm.name 	= item_data['name']
		itm.id 		= item_data['id']
		itm.url 	= "https://yw-web.yoworld.com/cdn/items/${n[..2]}/${n[2..4]}/${n}/${n}_60_60.gif"
	}

	return itm
}