<!-- This script is run when the user clicks on an "Add to cart" button. -->
<?php

$products = unserialize($_POST['products']);

$productToBeAdded = $_POST['productName'];
$productPrice = $products[$productToBeAdded];

// convert json file to array
if (file_exists("../cart.json")){
    $json = file_get_contents("../cart.json");
    $jsonArray = json_decode($json, $associative=true);
} 
else {
    $jsonArray = array();
};

// what to do when there is already one of more instances of the product in the cart 
if (isset($jsonArray[$productToBeAdded])) {
    $jsonArray[$productToBeAdded]['quantity'] = $jsonArray[$productToBeAdded]['quantity'] + 1;
    $jsonArray[$productToBeAdded]['total'] = $jsonArray[$productToBeAdded]['quantity'] * $productPrice;        
} 
// what to do when an instance of the product is not yet in the cart
else {
    $jsonArray[$productToBeAdded] = [
        'price' => $productPrice,
        'quantity' => 1,
        'total' => $productPrice
    ];
};

// convert array back into json format and save
file_put_contents('../cart.json', json_encode($jsonArray, JSON_PRETTY_PRINT));

header("Location: ../index.php");

