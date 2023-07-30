import os

pub struct Item
{
	pub mut:
		name		string
		id			int
		url			string
		price		string
		update		string
}

pub struct YoGuide
{
	pub mut:
		item		[]Item
		found		[]Item
}

pub fn build_guide() YoGuide
{
	mut yg := YoGuide{}
	mut lines = os.read_lines("items.txt") or { [''] }

	for line in lines
	{
		if line.len < 5 { continue }
		info := line.replace("(", "").replace(")", "").replace("'", "").split(",")

		if info.len == 5
		{
			yg.items << Item{
				name: info[0],
				id: info[1],
				url: info[2],
				price: info[3],
				update: info[4]
			}
		}
		else { println("[ X ] Error, Unable to parse line | ${line}") }
	}

	return yg
}

pub fn (mut yg YoGuide) new_item([]string arr) Item
{
	yg.name = arr[0]
	yg.id = arr[1].int()
	yg.url = arr[2]
	yg.price = arr[3]
	yg.update = arr[4]
}