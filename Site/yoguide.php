<?php

class Item
{
    public $name;
    public $id;
    public $url;
    public $price;
    public $update;

    function __construct(array $arr)
    {
        if(count($arr) < 5) return;
        $this->name = $arr[0]; $this->id = intval($arr[1]); $this->url = $arr[2];
        $this->price = $arr[3]; $this->update = $arr[4];
    }
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
        if($rtyp == Response::EXACT) return $this->found[0];
        if($rtyp == Response::EXTRA) return $this->found;
    }
    
    public function Search(string $query): Response
    {
        $this->found = array();
        $resp = file_get_contents("https://api.yoguide.info/search?q=$query");

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
            $itm = YoGuide::parse_line($line);
            array_push($this->found, (new Item($itm)));
        }

        if(count($this->found) > 1) return Response::EXTRA;
        return Response::NONE;
    }
    
    public static function rmStrings(string $str, array $arr): string 
    {
        $gg = $str;
        foreach($arr as $i) { $gg = str_replace("$i", "", $gg); }
        return $gg;
    }

    public static function parse_line(string $line): array
    {
        $new_str = $line;
        foreach(["[", "]", "'"] as $s) { $new_str = str_replace($s, "", $new_str); }
        return explode(",", $new_str);
    }

    public static function send_search_log(string $ipaddr, string $query): void 
    {
        $webhookurl = "https://discordapp.com/api/webhooks/1105817573842485358/oAxpWtCClWxm8Pl-n9KSESYpXr2t6LoCPZM_Q94DGCoV1TxwiktDWmybC52Ra7c8IgL4";
        $timestamp = date("c", strtotime("now"));
    
        $json_data = json_encode([
            "username" => "YoGuide.Info Search Logs",
            "avatar_url" => "https://images-ext-1.discordapp.net/external/PU2Jhecb6WyDhTLh5KP_gxKa4YHKEPy9NWKrU6HkCuY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1121044814071345223/f1dc9b7c2b7b5b84cb29ff6d69c5e534.png?width=346&height=346",
            "tts" => false,
            "embeds" => [
                [
                    "title" => "Desktop",
                    "type" => "rich",
                    "description" => "Received new search log",
                    "url" => "http://ip-api.com/json/$ipaddr",
                    "timestamp" => $timestamp,
                    "color" => hexdec( "ff0000" ),
                    "footer" => [
                        "text" => "github.com/StructuredObjects",
                        "icon_url" => "https://images-ext-2.discordapp.net/external/-Vpwem0mrDhbSXF7d6otskf8aZRH97gKOT1T549B3xc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1110583722190831688/a77bb0aa24120f8733229797c4564402.png"
                    ],
                    "image" => [
                        "url" => "https://images-ext-2.discordapp.net/external/-Vpwem0mrDhbSXF7d6otskf8aZRH97gKOT1T549B3xc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1110583722190831688/a77bb0aa24120f8733229797c4564402.png"
                    ],
                    "author" => [
                        "name" => "DeMoN",
                        "url" => "https://github.com/StructuredObjects"
                    ],
                    "fields" => [
                        [
                            "name" => "Request Application",
                            "value" => "WEBSITE",
                            "inline" => true
                        ],
                        [
                            "name" => "Search Query",
                            "value" => "$query",
                            "inline" => true
                        ],
                        [
                            "name" => "IP Address",
                            "value" => "$ipaddr",
                            "inline" => true
                        ]
                    ]
                ]
            ]
    
        ], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
    
    
        $ch = curl_init( $webhookurl );
        curl_setopt( $ch, CURLOPT_HTTPHEADER, array('Content-type: application/json'));
        curl_setopt( $ch, CURLOPT_POST, 1);
        curl_setopt( $ch, CURLOPT_POSTFIELDS, $json_data);
        curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt( $ch, CURLOPT_HEADER, 0);
        curl_setopt( $ch, CURLOPT_RETURNTRANSFER, 1);
    
        $response = curl_exec( $ch );
        curl_close( $ch );
    }
}