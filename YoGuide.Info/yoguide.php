<?php

$ygAPI = "https://api.yoguide.info";

class Item 
{
    public $name;
    public $id;
    public $url;
    public $price;
    public $update;

    function __construct(array $arr)
    {
        $this->name = $arr[0]; $this->id = intval($arr[1]); $this->url = $arr[2];
        $this->price = $arr[3]; $this->update = $arr[4];
    }
}

class Response 
{
    public $type;
    public $result;
    function __construct(ResponseType $t, array | Item $r)
    {
        $this->type = $t;
        $this->result = $r;
    }
}

enum ResponseType
{
    case NONE;
    case EXACT;
    case EXTRA;
}

class YoGuide
{
    private $found;
    public function searchItem(string $query): Response
    {
        $this->found = array();
        if(strlen($query) < 2) 
            return (new Response(ResponseType::NONE, 0));

        $api_resp = file_get_contents("$ygAPI/search?q=$query");
        echo $api_resp;

        if(!str_starts_with($api_resp, "[") && str_ends_with($api_resp, "]"))
            return (new Response(ResponseType::NONE, 0));
        
        if(!str_contains($api_resp, "\n"))
            return (new Response(ResponseType::EXACT,  (new Item(explode(",", $api_resp)))));

        $lines = explode("\n", $api_resp);

        foreach($lines as $line)
        {
            if(strlen($line) < 5) continue;
            $info = explode(",", YoGuide::remove_strings($line, array("'", "]", "[")));
            if(count($info) > 5) {
                array_push($this->found, (new Item($info)));
            }
        }

        if(count($this->found) > 1)
            return(new Response(ResponseType::EXTRA, $this->found));

        return (new Response(ResponseType::NONE, 0));
    }

    public function getResults(ResponseType $r): array | Item 
    {
        if($r == ResponseType::EXACT) return $this->found[0];
        if($r == ResponseType::EXTRA) return $this->found;
        return array();
    }

    public static function remove_strings(string $str, array $arr): string 
    {
        $gg = $str;
        foreach($arr as $i)
        { $gg = str_replace("$i", "", $gg); }
        return $gg;
    }
}

$eng = new YoGuide();
$resp = $eng->searchItem("26295");
$r = $eng->getResults($resp);
echo "$r->name";

?>