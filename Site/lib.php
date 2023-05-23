<?php

class API
{
    public $url = "https://api.yoworld.site";
    public $searchEndpoint = "https://api.yoworld.site/search";
    public $advanceEndpoint = "https://api.yoworld.site/advance";
    public $changeEndpoint = "https://api.yoworld.site/change";
    public $stats = "https://api.yoworld.site/stats";
}

class Item 
{
    public $name;
    public $id;
    public $url;
    public $price;
    public $update;

    public function arr2item(array $arr): void
    {
        if(count($arr) != 5) return;
        $this->name = $arr[0]; $this->id = $arr[1]; $this->url = $arr[2];
        $this->price = $arr[3]; $this->update = $arr[4];
    }
}

class YoworldSite
{
    public static function searchItem(string $query): array
    {
        if(strlen($query) == 0) return [];
        $results = file_get_contents((new API())->searchEndpoint. "?q=". $query);

        if($results === "[ X ] Error, You must fill all parameters to continue!") return [];
        if(str_contains($results, "No items found")) return [];
        if(!str_starts_with($results, "[") && !str_ends_with($results, "]")) return [];
        if(!str_contains($results, "\n")) 
        {
            $info = (new Utils())->parse_line($results);
            $itm = new Item();
            $itm->arr2item($info);
            return [$itm];
        }

        $lines = explode("\n", $results);
        $found = [];

        foreach($lines as $line)
        {
            if(strlen($line) < 5) continue;
            $info = (new Utils())->parse_line($line);
            $new_item = new Item();
            $new_item->arr2item($info);
            array_push($found, $new_item);
        }

        return $found;
    }
}

class Utils
{
    public static function parse_line(string $line): array
    {
        $new_str = $line;
        foreach(["[", "]", "'"] as $s)
        {
            $new_str = str_replace($s, "", $new_str);
        }
        return explode(",", $new_str);
    }

    public static function remove_strings(string $str, array $arr): string
    {
        $new_str = $str;
        foreach($arr as $s)
        {
            $new_str = str_replace($s, "", $new_str);
        }
        return $new_str;
    }
}

?>