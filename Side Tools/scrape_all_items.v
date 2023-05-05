/*
	YoworldDB Item Scraper Using Web Page & API

	Created in V due to performance

	@author: ArroGant SnF
	@since: 3/25/23
*/
import os
import x.json2
import net.http

pub const (
	yoworlddb_items_url = "https://yoworlddb.com/items/page/"
	yoworlddb_item_info_url = "https://yoworlddb.com/scripts/getItemInfo.php"
)

pub struct Item 
{
	pub mut:
		name				string
		id					int
		price				string
		img_url				string
}

pub struct Page
{
	pub mut:
		items			[]Item
		total_item		int
}

pub struct Scrape
{
	pub mut:
		data				string
		items				[]Item
		
		page_count			int
}

pub fn start_scraper() Scrape
{
	mut s := Scrape{}
	check_pages := http.get_text(yoworlddb_items_url)

	// Getting the max pages listed from combobox on the page.
	for page in check_pages.split("\n")
	{
		if page.contains("</select>") { break }
		if check_pages.trim_space().contains("option value=") 
		{	
			s.page_count = page.trim_space().replace("<option value=\"", "").replace(" >", "").replace("</option>", "").split("\"")[0].int()
		}
	}

	if s.page_count == 0 {
		print("[ x ] Error, Unable to get max pages of items...!\n")
		exit(0)
	}

	print("[ + ] Scraping ${s.page_count} pages....!\n")
	return s
}

pub fn (mut s Scrape) scrape()
{
	for i in 0..s.page_count
	{
		s.page = i
		page_content := http.get_text("${yoworlddb_items_url}${i}")
		s.scrape_page(page_content)
	}
}

pub fn (mut s Scrape) scrape_page(content string)
{
	page_lines := content.split("\n")

    mut item_name := ""
    mut item_id := 0
    mut item_image := ""
    mut item_price := "0"

    mut item_count := 0
    for line in page_lines
    {
		info = false
            if line.contains("<a class=\"item-image\"")
            {
				item_id, item_image, item_name = s.scrape_item(line, page_lines[c+2])
            }

            if item_name != "" && item_id > 0 && item_image != ""
			{
                    s.items << (Item{name: item_name, id: item_id, img_url: item_image, price: item_price})
                    s.data += "('${item_name}','${item_id}','${item_image}','${item_price}')\n"
                    item_name = ""
                    item_id = 0
                    item_image = ""
                    item_count++
					print("#${item_count}: ${item_name} | ${item_id} | ${item_price}\n")
            }
    }
	print("Page ${s.page} completed with ${item_count} | Recieved Item Info: ${all_info}....!\n")
}

pub fn (mut s Scrape) scrape_item(line string, line_two string) (string, string, string)
{
    item_id = line.split("data")[1].replace("=\"", "").replace("\"></a>", "").split("/")[3].replace(".gif", "").replace("_60_60", "").int()
    item_image = "https://yw-web.yoworld.com/cdn/items/" + line.trim_space().split("data=\"")[1].replace("\"></a>", "")
    item_name = line_two.replace("</a>", "").trim_space().replace("~ ", "").replace("'", "").replace(",", "")
	
	return item_id, item_image, item_name
}

fn main() {
	mut s := start_scraper()
	s.scrape()
	os.write_file("test.txt", s.data) or { return }
}