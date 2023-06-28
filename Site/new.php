<?php

class Item 
{
    public $name;
    public $id;
    public $url;
    public $price;
    public $update;
}

enum Response
{
    case NONE;
    case EXACT;
    case EXTRA;
}

class YoGuide
{
    private $found;

    public function getResults(Response $rtyp): Item | array 
    {
        if($rtyp == Response::NONE) return array('');
        if($rtyp == Response::EXACT) return $this->found;
        if($rtyp == Response::EXTRA) return $this->found;
    }
    
    function search(string $query): Response
    {
            $found = array();
            $resp = file_get_contents("https://api.yoguide.info/search?q=26295");
    
            echo "\x1b[31mResponse Test\x1b[0m: ". $resp. "\n";
            if(!str_starts_with($resp, "[") && !str_ends_with($resp, "]"))
                    die("[ X ] Unable to connect to YoGuide's API");
    
            if(!str_contains($resp, "\n"))
            {
                    $info = YoGuide::parse_line($resp);
                    array_push($this->found, (new Item($info))); // APPEND TO $this->found!
                    return Response::EXACT;
            }
    
            $lines = explode("\n", $resp);
    
            foreach($lines as $line)
            {
                    $info = YoGuide::parse_line($resp);
                    array_push($found, (new Item($info)));
            }
    
            if(count($found) > 1) return Response::EXTRA;
            return Response::NONE;
    }
    

    public function arr2item(array $arr): Item
    {
        $item = new Item();
        if(count($arr) != 5) return $item;
        $item->name = $arr[0]; $item->id = $arr[1]; $item->url = $arr[2];
        $item->price = $arr[3]; $item->update = $arr[4];
        return $item;
    }
    
    public static function rmStrings(string $str, array $arr): string 
    {
        $gg = $str;
        foreach($arr as $i) 
        { $gg = str_replace("$i", "", $gg); }
        return $gg;
    }

    public static function parse_line(string $line): array
    {
        $new_str = $line;
        foreach(["[", "]", "'"] as $s)
        {
            $new_str = str_replace($s, "", $new_str);
        }
        return explode(",", $new_str);
    }
}