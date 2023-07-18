<?php
include("yoguide.php");

$eng = new YoGuide();
$r = $eng->Search("cupids bow");
$results = $eng->getResults($r);

if($r == Response::NONE) {
    echo "[ X ] Unable to find item...!";
    return;
} else if($r == Response::EXACT) {

    echo "API Response: Response::EXACT";
    echo $results->name; " | ". $results->id; " | ". $results->price. " | ". $results->update;
} else if ($r == Response::EXTRA) {

    echo "API Response: Response::EXTRA\r\n";
    $c = 0;
    foreach($results as $itm)
    {
        if($itm->name != NULL && $itm->name != "") echo $itm->name. " | ". $itm->id. " | ". $itm->price. " | ". $itm->update. "\r\n";
    }
}