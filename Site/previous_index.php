<?php include("yoguide.php"); ?>
<html>

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles.css">
    <meta name="description" content="The Official #1 Price Guide For Yoworld Items. Helping the yoworld community prevent scams!">
    <meta name="author" content="MbF DeMoN">
    <title> YoPriceGuide </title>
</head>
<!-- Top Navigation Bar -->
<div class="top-bar">
    <!-- Main Title -->
    <a href="index.php"><img style="padding-right: 30px;" height="70" width="70" src="https://images-ext-2.discordapp.net/external/ryyteXeyYTZR1gEPQX5vsBPyLcwtU94zXVB599qvKzI/%3Fsize%3D1024/https/cdn.discordapp.com/icons/908592606634729533/1c930d9f6b53d79d5e1150d131d0f421.png?width=346&height=346" /></a>
    <!-- <h1 class="title">YoGuide</h1> -->
  
    <!-- Quick Search Bar -->
    <form style="display: inline-block;" method="post">
      <input class="txt-input" type="text" id="item_name" name="item_name" placeholder="Cupids Bow and Arrow" />
      <input class="btn-input" type="submit" name="search_item" id="search_item" value="Search"/>
    </form>
  
    <div class="nav-start">
      <a href="index.php"><button class="nav-option" type="submit">Home</button></a>
      <a href="https://discord.gg/guide"><button class="nav-option" type="submit">Discord Server</button></a>
    </div>
  </div>

  <?php
    
    if(array_key_exists("search_item", $_POST))
    {
      $query = $_POST['item_name'];
      $ip = $_SERVER["HTTP_CF_CONNECTING_IP"];

      if(empty($query)) echo "<p>Type an Item name or ID to search!";

      $eng = new YoGuide();
      $r = $eng->Search("cupids bow");
      $results = $eng->getResults($r);

      if($r == Response::NONE)
      {
        echo "No items found with your search query......!";
      } else if($r == Response::EXACT)
      {
        echo '<div class="result_box">';
        echo '<div class="grid-container">';
        echo '<div class="grid-item">';
        echo '<p class="item-name" style="font-size: 15px; color: #fff">'. $results->name. '</p>';
        echo '<img style="padding-top: 20px;" src="'. $results->url. '" />';
        echo '<p style="font-size: 15px;color: #fff">#'. $results->id. '</p>';
        echo '<p style="font-size: 15px;color: #fff">Price: '. $results->price. '</p>';
        echo '</div>';
        echo '</div>';
        echo '</div>';
      } else if($r == Response::EXTRA)
      { 
        echo '<div class="result_box">';
        echo '<div class="grid-container">';
        foreach($results as $item)
        {
          echo '<div class="grid-item">';
          echo '<p class="item-name" style="font-size: 15px; color: #fff">'. $item->name. '</p>';
          echo '<img style="padding-top: 20px;" src="'. $item->url. '" />';
          echo '<p style="font-size: 15px;color: #fff">#'. $item->id. '</p>';
          echo '<p style="font-size: 15px;color: #fff">Price: '. $item->price. '</p>';
          echo '</div>';
        }
        echo '</div>';
        echo '</div>';
      }
      
      YoGuide::send_search_log($ip, $query);
    }
    ?>
</body>
<style>
  *{
    color:white;
  }
</style>
</html>