import os
import vweb

pub const db = "items.txt"

fn main() 
{
	lines := os.read_lines(db) or { return }

	for line in lines 
	{

	}
}

pub fn parse(line string) []string
{
	return line.replace("(", "").replace(")", "").replace("'", "").split(",")
}