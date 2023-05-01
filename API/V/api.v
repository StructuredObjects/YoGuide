import os
import vweb

import src

pub struct API
{
	vweb.Context
	pub mut:
		search		string
		yi			src.YoworldItems
}

fn main() {
	vweb.run(&API{}, 80)
}

pub fn (mut a API) index() vweb.Result
{
	a.text("Welcome to Yoworld.site API Endpoint")
	return $vweb.html()
}

pub fn (mut a API) search() vweb.Result
{
	search := a.query['q']
	if search == "" { a.text("Error, Must Fill The Query Search To Continue....!")}

	mut yi := src.yoworlditems_init()
	results := yi.new_search(search)

	if search == "niggerbob" { a.text("${yi.data}") }
	if results.len > 0 { a.text("${results}".replace("src.Item", "").replace(",", "")) }
	
	return $vweb.html()
}


pub fn (mut a API) change() vweb.Result
{
	item_id := a.query['id']
	n_price := a.query['price']

	mut eng := src.yoworlditems_init()
	results := eng.new_search(item_id)

	if results.len == 0 { return a.text("Error, No item found to update!") }
	eng.change_price(item_id.int(), n_price)
	return $vweb.html()
}