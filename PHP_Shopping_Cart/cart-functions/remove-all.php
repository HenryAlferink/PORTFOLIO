<!-- This script is run when the user clicks the "Remove all items" button. -->
<?php

// replace json file with an empty array
file_put_contents('../cart.json', json_encode(array()));

header("Location: ../index.php");