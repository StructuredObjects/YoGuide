import os

fn main()
{
	mut main_db := os.read_file("items.txt") or { panic("Error reading items.txt") }
	new_item_db := os.read_file("test.txt") or { panic("Error reading test.txt") }

	lines := new_item_db.split("\n")
	for line in lines
	{
		if line.len < 5 { break }
		info := parse_line(line)
		if info.len == 4
		{
			check := main_db.contains(info[1])
			println("Checking ${info[0]}/${info[1]} | ${check}")
			if main_db.contains(info[1]) {}
			else {
				main_db += "('${info[0]}','${info[1]}','${info[2]}','0','0')\n"
			}
		}
	}
	os.write_file("updated.txt", main_db) or { return }
}

pub fn parse_line(line string) []string
{
	return line.replace("(", "").replace(")", "").replace("'", "").split(",")
}