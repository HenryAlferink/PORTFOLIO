<?php   

// Author: Henry Alferink
// Date: 21/06/2021

// Credit: In creating this website, I found this video very useful, 
// particularly regarding storing information in the json format:
// https://www.youtube.com/watch?v=NxeNqHdJFxs

/*
Assumption on $products array:
    The name of each product is unique. Therefore it can
    be used as an index.
*/

// Feel free to modify this array
$products = [
    [ "name" => "Sledgehammer", "price" => 125.75   ],
    [ "name" => "Axe",          "price" => 190.50   ],
    [ "name" => "Bandsaw",      "price" => 562.131  ],
    [ "name" => "Chisel",       "price" => 12.9     ],
    [ "name" => "Hacksaw",      "price" => 18.45    ],
];

include "shopping-cart-page.php";

$productListComponent = new ProductListComponent($products);
$productListHTML = $productListComponent->getProductListHTML();

$cartComponent = new CartComponent();
$cartHTML = $cartComponent->getCartHTML();

$page = new ShoppingCartPage($productListHTML, $cartHTML);
