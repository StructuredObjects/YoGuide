module yg

import os
import time

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
	mut:
		query			string

	pub mut:
		items		[]Item
		found		[]Item
}

pub enum ResultType
{
	_none					= 0
	_exact 					= 1
	_extra 					= 2
	_item_failed_to_update	= 3
	_item_updated			= 4
}

pub struct Response
{
	pub mut:
		r_type		ResultType
		results		[]Item
}

pub fn yg_init() YoGuide
{
	/*
		Reading a file with item information in lines with the following syntax

		('ITEM_NAME','ITEM_ID','ITEM_IMGURL','ITEM_PRICE','ITEM_LASTUPDATE')
	*/
	mut yg 		:= YoGuide{}
	items_db 	:= os.read_lines("items.txt") or { [] }
	if items_db == [] { return YoGuide{} } // if yg_init() == YoGuide{} { println("no db or items found...!") }

	for line in items_db 
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

pub fn (mut yg YoGuide) is_id_in_db(id int) bool 
{
	for item in yg.items 
	{ if item.id == id { return true } }
	return false
}

pub fn add_new_item(arr []string) bool 
{
	if arr.len != 5 { return false }
	mut file := os.open_append(item_filepath) or { return false }
	file.write("('${arr[0]}','${arr[1]}','${arr[2]}','${arr[3]}','${arr[4]}')\n".bytes()) or { return false }
	file.close()
	return true
} 

pub fn (mut yg YoGuide) search(q string) Response
{
	yg.query = q
	if q.int() > 0 {
		yg.found = [yg.search_by_id()]
		if yg.found[0].name != "" {
			return Response{r_type: ResultType._exact, results: yg.found}
		}

		new_item := retrieve_item_info(Item{id: yg.query.int()}, true)
		if new_item.name != "" {
			retrieve_item_ywinfo_price(new_item, false)
			return Response{r_type: ResultType._exact, results: yg.found}
		}

		return Response{r_type: ResultType._none}
	}

	yg.search_by_name()

	if yg.found.len == 1 && yg.found[0].name != "" { 
		return Response{r_type: ResultType._exact, results: yg.found}
	}
	
	if yg.found.len > 1 { return Response{r_type: ResultType._extra, results: yg.found} }

	return Response{r_type: ResultType._none}
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

pub fn (mut yg YoGuide) update_item(itm Item, new_price string) ResultType
{
	mut found 		:= ResultType._item_failed_to_update
	mut new_db 		:= ""
	current_time 	:= "${time.now()}".replace("-", "/").replace(" ", "-")

	for item in yg.items
	{
		if item.id == itm.id {
			new_db 	+= "('${item.name}','${item.id}','${item.url}','${new_price}','${current_time}')\n"
			found 	= ResultType._item_updated
		} else {
			new_db 	+= "('${item.name}','${item.id}','${item.url}','${item.price}','${item.update}')\n"
		}
	}

	os.write_file(item_filepath, new_db) or { 0 }

	return found
}

/*
import os
import yoguide

fn main() {
	mut yg := yoguide.yg_init()

	query := os.input("Item name or ID: ")

	r := yg.search(query)

	if r.r_type == ._none {
		println("[ X ] No items were found in DB....!")

		if query.int() > 0 {
			println("[ + ] Requesting yoworlddb.com for information...!")
			item := yoguide.retrieve_item_info(yoguide.Item{id: query}, true)
			if item.name == "" 
			{ 
				println("[ X ] Unable to retrieve information from yoworlddb.com or they do not have information for the item....!")
				exit(0)
			}
			println("[ + ] Item: ${item.name} | ${item.id} | ${item.price} | ${item.update}")
		}

	} else if r.r_type == ._exact { /* VALID ITEM IDS WILL ALWAYS FALL HERE */
		yoguide.retrieve_item_info(mut r.results[0], false)
		yoguide.retrieve_item_ywinfo_price(mut r.results[0], false)
		println("Item: ${r.results[0].name} | ${r.results[0].id} | ${r.results[0].price} | ${r.results[0].update}")

	} else if r.r_type == ._extra {
		for item in r.results
		{
			println("Item: ${item.name} | ${item.id} | ${item.price} ${item.update}")
		}
	}

	/* Updating an item (Only works with Item ID for exact item) */
	update_check := yg.update_item(r.results[0], "400m")
	if update_check == false {
		println("[ X ] Error, Unable to update item...!")
		exit(0)
	}

	println("[ + ] Item ${r.results[0].name} successfully updated...!")
}

*/