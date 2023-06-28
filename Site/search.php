<?php
include("new.php");

$eng = new YoGuide();
$r = $eng->Search($argv[1]);
$results = $eng->getResults($r);
var_dump($r);
var_dump($results);
echo $results->name;

if($r == Response::NONE) {
    echo "[ X ] Unable to find item...!";
    return;
} else if($r == Response::EXACT) {
    echo "EXACT";
} else if ($r == Response::EXTRA) {
    echo "EXTRA";
}