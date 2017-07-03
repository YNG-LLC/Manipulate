<?php
session_start();

$db_host = 'something';
$db_username = 'something';
$db_pass = 'something';
$db_tablename = 'something';

$dbConnection = new mysqli($db_host, $db_username, $db_pass, $db_tablename);
if(!$dbConnection){
    echo "died1";
	die('Mysql connection error: ' . mysqli_connect_error());
}
if ($dbConnection->connect_error) {
    echo "died2";
    die("Connection failed: " . $conn->connect_error);
}

?>
