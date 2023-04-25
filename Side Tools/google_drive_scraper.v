import net.http

fn main() {
	drive_results := http.get_text("https://docs.google.com/spreadsheets/d/e/2PACX-1vQRR3iveCH4Y1pdxWCAzW7qchTlHYzvlNG6e6ZyMKn2vjodu8-uLSoAHSLMq1X3qA/pubhtml")
	lines := drive_results.split("</td>")
	mut last_item := ""
	for line in lines
	{
		if line.ends_with(">") { continue }
		if line.starts_with("</tr>") { continue }
		if line.contains("<td class=\"s3\" dir=\"ltr\">") {
			last_item = line.split(">")[1]
		} else if line.contains("<td class=\"s6\" dir=\"ltr\">") || line.contains("<td class=\"s7\" dir=\"ltr\">") {
			if line.split(">")[1].trim_space() != "TBD" {
				if line.split(">")[1].trim_space().contains("-") {} else {
					println("${last_item} ${line.split(">")[1]}")
				}
			}
		}
	}
}