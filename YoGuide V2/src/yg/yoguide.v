module yg

import os

const item_filepath = "/root/api/items.txt"

pub struct Item
{
	pub mut:
		/*
			General Item Information
		*/
		name				string
		id					int
		url					string
		price				string
		update				string

		/*
			Actions you can do with the ITEM
		*/
		is_tradable			int
		is_giftable			int

		/*
			In-store Information
		*/
		in_store			bool
		store_price			string
		gender				string
		xp					string
		category			string

		/*
			Extra Info
		*/
		yw_info_price		string
		yw_info_update		string
		yw_info_approval	string
		yw_db_price			string
}

pub struct YoGuide
{
	query			string

	pub mut:
		items		[]Item
		found		[]Item
}

pub enum ResultType
{
	NONE					= 0
	EXACT 					= 1
	EXTRA 					= 2
	ITEM_FAILED_TO_UPDATE	= 3
	ITEM_UPDATED			= 4
}

pub struct Response
{
	pub mut:
		r_type		ResultType
		results		[]Item
}

pub fn yg_init() YoGuide
{
	mut yg 		:= YoGuide{}
	items_db 	:= os.read_lines("items.txt") or { [] }
	if item_db == [] { return YoGuide{} } // if yg_init() == YoGuide{} { println("no db or items found...!") }

	for line in lines 
	{
		if line.len < 4 { continue }
		info := line.replace("(", "").replace(")", "").replace("'", "").split(",")
		if info.len == 5
		{
			yg.items << Item {
				name: 	info[0],
				id: 	info[1].int(),
				url: 	info[2],
				price: 	info[3],
				update: info[4]
			}
		} else { println("[ X ] Warning, Unable to parse line\n${line}") }
	}

	return yg
}

pub fn (mut yg YoGuide) search(string q) Response
{
	yg.query = q
	if q.int() > 0 {
		yg.found = [yg.search_by_id()]
		if yg.found[0].name != "" {
			return Response{r_type: ResultType.EXACT, results: yg.found}
		}

		return Response{r_type: ResultType.NONE}
	}

	yg.search_by_name()

	if yg.found.len == 1 && yg.found[0] != "" { 
		return Response{r_type: ResultType.EXACT, results: yg.found}
	}
	
	if yg.found.len > 1 { return Response{r_type: ResultType.EXTRA, results: yg.found} }

	return Response{r_type: ResultType.NONE}
}

fn (mut yg YoGuide) search_by_name() []Item
{
	yg.found = []
	for item in yg.items
	{
		if item.name == yg.query || (item.name).to_lower() == (yg.query).to_lower() { 
			return [item] 
		}

		if (item.name).to_lower().contains(yg.query.to_lower()) {
			yg.found << item
		}
	}

	return yg.found
}

fn (mut yg YoGuide) search_by_id() Item
{
	for item in yg.items
	{
		if item.id == yg.query.int() { return item }
	}

	return Item{}
}

pub fn (mut yg YoGuide) update_item(Item itm, string new_price) ResultType
{
	mut found 		:= ResultType.ITEM_FAILED_TO_UPDATE
	new_db 			:= ""
	current_time 	:= "${time.now()}".replace("-", "/").replace(" ", "-")

	for item in yg.items
	{
		if item.id == itm.id {
			new_db 	+= "('${item.name}','${item.id}','${item.url}','${new_price}','${current_time}')\n"
			found 	= ResultType.ITEM_UPDATED
		} else {
			new_db 	+= "('${item.name}','${item.id}','${item.url}','${item.price}','${item.update}')\n"
		}
	}

	os.write_file(item_filepath, new_db) or { 0 }

	return found
}