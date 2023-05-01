module src

import os

pub type ItemResults = Item | []Item | []string

pub struct Item 
{
	pub mut:
		name 			string
		id 				int
		url				string
		price			string
		last_updated	string
}

pub struct YoworldItems
{
	pub mut:
		data		string
		lines		[]string
		items		[]Item
		found		[]Item

		search		string
		results	 	Results
}

pub struct Results
{
	pub mut:
		match_found				bool
		match_found_results		Item
}

pub fn yoworlditems_init() YoworldItems
{
	mut yi := YoworldItems{results: &Results{}}
	yi.data = os.read_file("items.txt") or { "" }
	yi.lines = yi.data.split("\n")
	yi.fetch_all_items()
	return yi
}

pub fn (mut yi YoworldItems) new_search(s string) []Item
{
	yi.search = s
	if yi.search.int() > 0 {
		return [yi.search_by_id()]
	}
	return yi.search_by_name()
}

pub fn (mut yi YoworldItems) fetch_all_items()
{
	for line in yi.lines
	{
		if line.len < 5 { continue }
		info := parse_line(line)
		yi.items << Item{name: info[0], id: info[1].int(), url: info[2], price: info[3], last_updated: info[4]}
	}
}

pub fn (mut yi YoworldItems) bulk_items_found_check() bool
{
	if yi.found.len > 0 { return true }
	return false
}

pub fn (mut yi YoworldItems) search_by_name() []Item
{
	for item in yi.items
	{
		no_case_sen := yi.search.to_lower()
		if item.name == yi.search { return [item] }
		if item.name.contains(no_case_sen) { return [item] }

		if no_case_sen.contains(" ") {
			words := yi.search.split(" ")
			mut matched_words := 0
			if words.len < 2 {
				for word in words {
					if item.name.contains(word) { yi.found << Item{name: item.name, id: item.id, url: item.url, price: item.price, last_updated: item.last_updated} }
				}
			} else {
				for word in words {
					if item.name.contains(word) { matched_words++ }
					if matched_words > 1 { yi.found << Item{name: item.name, id: item.id, url: item.url, price: item.price, last_updated: item.last_updated} }
				}
			}
		}
	}
	return yi.found
}

pub fn (mut yi YoworldItems) search_by_id() Item
{ for item in yi.items { if "${item.id}" == "${yi.search}" { return item } } 
return Item{} }

pub fn (mut yi YoworldItems) change_price(item_id int, new_price string) bool
{
	mut new_db := ""
	mut found := false
	
	lines := os.read_lines("/root/bot/items.txt") or { [] }
	time_now := os.execute("date +\"%M/%d/%Y-%I:%m:%S\"").output

	for line in lines
	{
		if line.len < 5 { continue }
		info := parse_line(line)
		if info[1].int() == item_id { 
			new_db += "('${info[0]}','${info[1]}','${info[2]}','${new_price}','${time_now}')\n"
			found = true
		} else { new_db += "${line}\n" }
	}

	os.write_file("items.txt", new_db) or { return false }
	return found
}