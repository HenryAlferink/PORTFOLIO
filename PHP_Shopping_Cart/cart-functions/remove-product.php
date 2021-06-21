<!-- This script is run when the user clicks on a "Remove from cart" button. 
Note that we can safely assume that the product to be deleted does exist in
the json file, so we don't need to do any error checking in that regard. -->

<?php

$jsonArray = unserialize($_POST['jsonArray']);
$productToBeRemoved = $_POST['productName'];

// what to do when there is more than one instance of the product in the cart
if ($jsonArray[$productToBeRemoved]['quantity'] > 1){
    $jsonArray[$productToBeRemoved]['quantity'] -= 1;
    $jsonArray[$productToBeRemoved]['total'] -= $jsonArray[$productToBeRemoved]['price'];
}
// what to do when there is only one instance of the product in the cart
else {
    unset($jsonArray[$productToBeRemoved]);
}

file_put_contents('../cart.json', json_encode($jsonArray, JSON_PRETTY_PRINT));

header("Location: ../index.php");