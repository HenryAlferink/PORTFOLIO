<?php    
/* sprintf("%.2f", round(...)) ensures that we are rounding to 2 D.P. */


class ShoppingCartPage {
    function __construct($productListHTML, $cartHTML) {       
        $this->renderPage($productListHTML, $cartHTML);
    }

    function renderPage($productListHTML, $cartHTML) {
        echo "
            <!DOCTYPE html>
            <html lang='en'>
            <head>
                <meta charset='UTF-8'>
                <meta http-equiv='X-UA-Compatible' content='IE=edge'>
                <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                <title>Document</title>
            </head>
            <body>
                <h1>Shopping Cart</h1>
                <hr>
                <h3>Product List</h3>
                $productListHTML
                <hr>
                <h3>Cart</h3>
                $cartHTML
            </body>
            </html>
        ";
    }    
}


class ProductListComponent {
    function __construct($products){
        $this->products = $products;
        $this->convertProducts = $this->convertProductList();
    }

    // convert products array to a key:value array with key=product name,
    // value=product price. This makes for easier access of the price of
    // a given product.
    function convertProductList() {
        $convertedProducts = array();
        foreach ($this->products as $product) {
            $convertedProducts[$product['name']] = $product['price']; 
        };
        return $convertedProducts;
    }

    function getProductListHTML() {
        $htmlString = "
            <table border=1>
            <tr>
                <th>Product</th>
                <th>Price</th>
            </tr>
        ";

        for ($i=0; $i < count($this->products); $i++) { 
            $productName = $this->products[$i]["name"];
            $productPrice = $this->products[$i]["price"];
            $productPriceRounded = sprintf("%.2f", round($productPrice, 2));
            
            // this allows the array to be passed through the $_POST variable to a different page
            $serializedProductsArray = serialize($this->convertProducts);         

            $htmlString .= "
                <tr>
                    <td>$productName</td>
                    <td>\$$productPriceRounded</td>
                    <td><form action='cart-functions/add-product.php' method='post'>
                        <button type='submit' name='productName' value=$productName>Add to cart</button>
                        <input type='hidden' name='products' value=$serializedProductsArray>
                    </form></td>
                </tr>
            ";
        }
        return $htmlString . "</table>";
    }
}


class CartComponent {
    function getCartHTML() {     
        $htmlString = "";
        
        if (file_exists("cart.json")) {
            $json = file_get_contents("cart.json");
            $jsonArray = json_decode($json, $associative=true);

            // this allows the array to be passed through the $_POST variable to a different page
            $serializedJsonArray = serialize($jsonArray);
            
            if (isset($jsonArray) and !$jsonArray == []) {
                $htmlString .= "
                    <table border=1>
                    <tr>
                        <th>Product</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Total</th>
                    </tr>
                ";

                foreach ($jsonArray as $product => $productInfo) {
                    $priceRounded = sprintf("%.2f", round($productInfo['price'], 2));
                    $totalRounded = sprintf("%.2f", round($productInfo['total'], 2));

                    $htmlString .= "
                        <tr>
                            <td>$product</td>
                            <td>\$$priceRounded</td>
                            <td>${productInfo['quantity']}</td>
                            <td>\$$totalRounded</td>
                            <td><form action='cart-functions/remove-product.php' method='post'>
                                <button type='submit' name='productName' value=$product>
                                    Remove from cart
                                </button>
                                <input type='hidden' name='jsonArray' value=$serializedJsonArray>
                            </form></td>
                        </tr>
                    ";
                }
                return $htmlString .
                    "</table>" .
                    $this->getRemoveAllButtonHTML() .
                    "<br><hr>" .
                    $this->getTotalAmountHTML();
            }
            else {
                return "No items in cart.";
            }
        }
    }

    function getRemoveAllButtonHTML(){
        return "
            <br>
            <form action='cart-functions/remove-all.php'>
                <button>Remove all items</button>
            </form>
        ";
    }

    function getTotalAmountHTML(){
        if (file_exists("cart.json")){
            $json = file_get_contents("cart.json");
            $jsonArray = json_decode($json, $associative=true);

            if (isset($jsonArray) and !$jsonArray == []){
                $total = 0;
                foreach ($jsonArray as $product => $productInfo) {
                    $total += $productInfo['total'];
                }

                $totalRounded = sprintf("%.2f", round($total, 2));
                
                return "
                    <table border=1>
                        <tr>
                            <th>Order total:</th>
                            <th>\$$totalRounded</th>
                        </tr>
                    </table>
                ";
            }
        }
    }
}