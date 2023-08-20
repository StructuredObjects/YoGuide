import os

const user_db = "assets/users.db"
pub struct User 
{
	pub mut:
		username	string
		key			string
		level		string
		ip_addr		string
}

pub fn find_user() User 
{
	/*
		('USERNAME','USERID','LEVEL','IP_ADDR')
	*/
	user_lines := os.read_lines("assets/uses.db") or { [] }

	for line in user_lines
	{
		if line.len < 5 { continue }
		info := line.replace("(", "").replace(")", "").replace("'", "").split(",")
		if info == 4
	}
}