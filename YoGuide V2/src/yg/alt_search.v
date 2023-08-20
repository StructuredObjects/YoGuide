module yg

import x.json2 as jsn
import net.http as web

pub fn (mut itm Item) retrieve_item_info(add_main bool) Item
{
	data := {'id': "${itm.id}"}
	resp := web.post_form("https://yoworlddb.com/scripts/getItemInfo.php", data) or { return itm }

	if resp.body.starts_with("{") == false && resp.body.ends_with("}") == false {
		println("[ X ] Warning, Unable to get the correct response from 'api.yoworld.info'....!")
		return itm
	}

	resp_obj 	:= (jsn.raw_decode("${jsn_obj}") or { return itm }).as_map()
	
	itm.gender 			= (resp_obj['gender'] or { "" }).str()
	itm.is_tradable 	= (resp_obj['is_tradable'] or { "" }).int()
	itm.is_giftable 	= (resp_obj['can_gift'] or { "" }).int()
	itm.category 		= (resp_obj['category'] or { "" }).str()
	itm.xp 				= (resp_obj['xp'] or { "" }).str()

	in_store := (jsn_obj['active_in_store'] or { "" }).str()
	if "${in_store}" == "1" { itm.in_store == true } else { itm.in_store = false }



	price_coins 	:= (jsn_obj['price_coins'] or { "" }).str()
	price_cash 		:= (jsn_obj['price_cash'] or { "" }).str()

	if add_main
	{
		itm.name 	= (jsn_obj['item_name'] or { "" }).str()
		itm.id 		= (jsn_obj['id'] or { "" }).int()
		itm.url 	= "https://yw-web.yoworld.com/cdn/items/${itm.id.str()[..2]}/${itm.id.str()[2..4]}/${itm.id}/${itm.id}_60_60.gif"
		
		if price_coins.int() > 0 {
			itm.yw_db_price = "${price_coins}c"
		} else if price_cash.int() > 0 {
			itm.yw_db_price = "${price_cash}yc"
		}
	}

	return itm
}

pub fn (mut itm Item) retrieve_item_ywinfo_price(add_main bool) Item
{
	resp := web.get_text("https://api.yoworld.info/api/items/${itm.id}")

	if resp.starts_with("{") == false && resp.ends_with("}") == false
	{ return itm }

	jsn_obj 	:= (jsn.raw_decode("${resp}") or { return itm }).as_map()
	data 		:= (jsn.raw_decode((jsn_obj['data'] or { "" }).str()) or { return itm }).as_map()
	item_data	:= (jsn.raw_decode((data['item']  or { "" }).str()) or { return itm }).as_map()
	price_prop	:= (jsn.raw_decode((item_data['price_proposal'] or { "" }).str()) or { return itm }).as_map()
	
    mut search 		:= false
    mut time 		:= ""
    mut price 		:= ""
    mut approved 	:= ""
	mut history 	:= map[string]string{}

    for line in "${price_prop}".replace(",", "\n").split("\n")
	{
        if line.contains("price_proposals") {
            search = true 
		}

        if search {
            if line.contains("updated_at: ") {
                time = line.replace("updated_at: ", "")
			}
            
            if line.contains("price: ") {
                price = line.replace("price: ", "")
			}
				
            if line.contains("username: ") {
                approved = line.replace("username: ", "")
                history[price] = "${time}//${approved}"
			}
		}
	}

	itm.yw_info_price 		= price
	itm.yw_info_update 		= time
	itm.yw_info_approval 	= approved

	if add_main {
		itm.name 	= (item_data['name'] or { "" }).str()
		itm.id 		= (item_data['id'] or { "" }).int()
		itm.url 	= "https://yw-web.yoworld.com/cdn/items/${itm.id.str()[..2]}/${itm.id.str()[2..4]}/${itm.id}/${itm.id}_60_60.gif"
	}

	return itm
}