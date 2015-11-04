<?php
$servername = "localhost";
$username = "zixian";
$password = "LiveFlight2014";
$dbname = "cs3103";

$where = " WHERE ";
$and = " AND ";
$or = " OR ";
$sql = "SELECT name, price, platform, cond, url, rtt FROM pricelist ";
$nameFilter = " name like ? ";
$conditionFilter = " cond=?";
$maxPriceFilter = " price<=? ";
$minPriceFilter = " price>=? ";
$platformFilter = " platform=? ";

$numParams = 0;
$params = array();
$bindFlags = "";
$conditions = "";

if(isset($_GET["searchTerm"]) && $_GET["searchTerm"]!=""){
    $numParams++;
    $bindFlags.="s";
    $conditions.=$nameFilter;
    array_push($params, "%".$_GET["searchTerm"]."%");
}

if(isset($_GET["platform"]) && $_GET["platform"]!=""){
    if($numParams>0) $conditions.=$and;
    $conditions.=$platformFilter;
    $numParams++;
    $bindFlags.="s";
    array_push($params, $_GET["platform"]);
}

if(isset($_GET["condition"]) && $_GET["condition"]!=""){
    if($numParams>0) $conditions.=$and;
    $conditions.=$conditionFilter;
    $numParams++;
    $bindFlags.="s";
    array_push($params, $_GET["condition"]);
}

if(isset($_GET["highPrice"]) && $_GET["highPrice"]!=""){
    if($numParams>0) $conditions.=$and;
    $conditions.=$maxPriceFilter;
    $numParams++;
    $bindFlags.="d";
    array_push($params, (double)$_GET["highPrice"]);
}

if(isset($_GET["lowPrice"]) && $_GET["lowPrice"]!=""){
    if($numParams>0) $conditions.=$and;
    $conditions.=$minPriceFilter;
    $numParams++;
    $bindFlags.="d";
    array_push($params, (double)$_GET["lowPrice"]);
}

// Construct prepared statement
$query = $sql;
if($numParams>0) $query.=$where.$conditions;
$bindParams = array();
$bindParams[] = $bindFlags;
for($i=0; $i<$numParams; $i++) $bindParams[] = &$params[$i];

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$stmt = $conn->prepare($query);
if($numParams>0) call_user_func_array(array($stmt, 'bind_param'), $bindParams);
$stmt->execute();
$result = $stmt->get_result();
$res = array();
while($row = $result->fetch_assoc()){
	array_push($res, $row);
}

$stmt->close();
$conn->close();
echo json_encode($res);
?>
