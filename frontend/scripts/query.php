<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "test";

$where = " WHERE ";
$and = " AND ";
$or = " OR ";
$sql = "SELECT name, price, platform, cond, url, rtt FROM pricelist ";
$nameFilter = " name like '%(?)%'";
$conditionFilter = " cond like '%(?)%'";
$priceFilter = " price>=(?) AND price<=(?) ";
$platformFilter = " platform='(?)' ";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$query = $sql;
if($_GET["searchTerm"]!=null && $_GET["searchTerm"]!=""){
	$query+=$nameFilter;
	$stmt = $conn->prepare($query);
	$stmt->bind_param('s', $_GET["searchTerm"]);
} else{
	$stmt = $conn->prepare($query);
}

$stmt->execute();

$result = $stmt->get_result();
$res = array();
while($row = $result->fetch_assoc()){
	array_push($res, $row);
}

// if ($result->num_rows > 0) {
//     // output data of each row
//     $res = array();
//     while($row = $result->fetch_assoc()) {
//         array_push($res, $row);
//     }
//     echo json_encode($res);

// } else {
//     echo "0 results";
// }
$stmt->close();
$conn->close();
?>
