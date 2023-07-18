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

    public static function send_search_log(string $ipaddr, string $query): void 
    {
        $webhookurl = "https://discordapp.com/api/webhooks/1105817573842485358/oAxpWtCClWxm8Pl-n9KSESYpXr2t6LoCPZM_Q94DGCoV1TxwiktDWmybC52Ra7c8IgL4";
        $timestamp = date("c", strtotime("now"));
    
        $json_data = json_encode([
            // Message
            // "content" => "Received new search log.",
            
            // Username
            "username" => "YoGuide.Info Search Logs",
    
            // Avatar URL.
            // Uncoment to replace image set in webhook
            "avatar_url" => "https://ru.gravatar.com/userimage/28503754/1168e2bddca84fec2a63addb348c571d.jpg?size=312",
    
            // Text-to-speech
            "tts" => false,
    
            // Embeds Array
            "embeds" => [
                [
                    // Embed Title
                    "title" => "Desktop",
    
                    // Embed Type
                    "type" => "rich",
    
                    // Embed Description
                    "description" => "Received new search log",
    
                    // URL of title link
                    "url" => "http://ip-api.com/json/$ipaddr",
    
                    // Timestamp of embed must be formatted as ISO8601
                    "timestamp" => $timestamp,
    
                    // Embed left border color in HEX
                    "color" => hexdec( "ff0000" ),
    
                    // Footer
                    "footer" => [
                        "text" => "github.com/StructuredObjects",
                        "icon_url" => "https://images-ext-2.discordapp.net/external/-Vpwem0mrDhbSXF7d6otskf8aZRH97gKOT1T549B3xc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1110583722190831688/a77bb0aa24120f8733229797c4564402.png"
                    ],
    
                    // Image to send
                    "image" => [
                        "url" => "https://images-ext-2.discordapp.net/external/-Vpwem0mrDhbSXF7d6otskf8aZRH97gKOT1T549B3xc/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1110583722190831688/a77bb0aa24120f8733229797c4564402.png"
                    ],
    
                    // Thumbnail
                    //"thumbnail" => [
                    //    "url" => "https://ru.gravatar.com/userimage/28503754/1168e2bddca84fec2a63addb348c571d.jpg?size=400"
                    //],
    
                    // Author
                    "author" => [
                        "name" => "DeMoN",
                        "url" => "https://github.com/StructuredObjects"
                    ],
    
                    // Additional Fields array
                    "fields" => [
                        // Field 1
                        [
                            "name" => "Request Application",
                            "value" => "WEBSITE",
                            "inline" => true
                        ],
                        // Field 2
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
                        // Etc..
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
        echo $response;
        // If you need to debug, or find out why you can't send message uncomment line below, and execute script.
        // echo $response;
        curl_close( $ch );
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