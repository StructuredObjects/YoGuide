import os
import net.http
import x.json2 as j

pub const db = "items.txt"

fn main() 
{
	lines := os.read_lines(db) or { return }

	mut new_db := ""

	mut c := 0
	for line in lines 
	{
		if line.len < 5 { continue }
		info := parse(line)

		req := http.post_form("https://yoworlddb.com/scripts/getItemInfo.php", {"iid": "${info[1]}"}) or { http.Response{} }
		if req.body == "" { continue }

		jobj := j.raw_decode(req.body) or { return }
		info_obj := j.raw_decode("${jobj.as_map()['response']}") or { return }
		item_info := info_obj.as_map()

		in_store := "${item_info['active_in_store']}"
		
		if in_store == "1" {
			mut price := "${item_info['price_coins']}c"

			if price == "0" || price == "0c" { price = "${item_info['price_cash']}yc" }
			new_db += "('${info[0]}','${info[1]}','${info[2]}','${price}','${info[4]}')"
			println("[ + ] ${c}/${lines.len} New Item Priced! '${info[0]}' ${price}")
		} else {
			new_db += line
			println("[ X ] ${c}/${lines.len} Item Skipped")
		}
		c++
	}

	os.write_file("testing.txt", new_db) or { return }
}

pub fn parse(line string) []string
{
	return line.replace("(", "").replace(")", "").replace("'", "").split(",")
}