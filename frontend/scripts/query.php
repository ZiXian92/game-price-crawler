<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "test";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT name, price, platform, cond, url, rtt FROM pricelist";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    $res = array();
    while($row = $result->fetch_assoc()) {
        array_push($res, $row);
    }
    echo json_encode($res);

} else {
    echo "0 results";
}
$conn->close();
?>
