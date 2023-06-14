<?php

function send_search_log(string $ipaddr, string $query) {
    $webhookurl = "https://discordapp.com/api/webhooks/1105817573842485358/oAxpWtCClWxm8Pl-n9KSESYpXr2t6LoCPZM_Q94DGCoV1TxwiktDWmybC52Ra7c8IgL4";
    $timestamp = date("c", strtotime("now"));

    $json_data = json_encode([
        // Message
        "content" => "Received new search log.",
        
        // Username
        "username" => "YoGuide.Info Search Logs",

        // Avatar URL.
        // Uncoment to replace image set in webhook
        "avatar_url" => "https://ru.gravatar.com/userimage/28503754/1168e2bddca84fec2a63addb348c571d.jpg?size=512",

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
    // If you need to debug, or find out why you can't send message uncomment line below, and execute script.
    // echo $response;
    curl_close( $ch );
}


send_search_log("5.5.5.5", "gg");