<?php 

include("search_controller.php"); 
$query = $_POST['item_name'] ?? null;
$ip = $_SERVER["HTTP_CF_CONNECTING_IP"];
$search = new search_controller;

?>
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

    <?php if(array_key_exists("search_item",$_POST)) : ?>

        <?php if(empty($query) || $query == null) : ?>
            <h1 style="color:red;">Please Provide A Name</h1>
            <?php else : ?>
                <?php 
                    $searching = $search->search($query);
                ?>
                <?php if($searching == false || !$search->fetch()) : ?>
                    <h1 style="color:red;">Sorry But Couldn't Find The Following Item</h1>
                    <?php else  :?>
                        <?php $items = $search->fetch()?>
                            <?php if(is_array($items)):?>
                                <div class="result_box">
                                <div class="grid-container">
                                    <?php foreach($items as $item) :?>
                                        <div class="grid-item">
                                            <h1><?=$item[0]?></h1>
                                            <img src="<?=substr($item[2],0,-4)?>" alt="product">
                                            <h1>Price : <span style="color:green;"><?=$item[1]?></span></h1>
                                            </div>
                                    <?php endforeach ;?>
                                </div>
                            </div>
                            <?php endif;?>
                        <?php endif;?>
                    
                <?php endif; ?>
            
        <?php endif;?>

  
</body>
<style>
  *{
    font-family: sans-serif;
  }
</style>
</html>