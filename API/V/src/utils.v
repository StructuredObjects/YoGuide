module src

pub fn parse_line(line string) []string { return line.replace("(", "").replace(")", "").replace("'", "").split(",") }