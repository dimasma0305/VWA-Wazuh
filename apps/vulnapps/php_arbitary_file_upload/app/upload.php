<?php
function wh_log($log_msg)
{
    $log_filename = "/var/log/app";
    $log_file_data = $log_filename.'/log_' . date('d-M-Y') . '.log';
    // if you don't add `FILE_APPEND`, the file will be erased each time you add a log
    file_put_contents($log_file_data, $log_msg . "\n", FILE_APPEND);
} 

if (filter_input(INPUT_SERVER, 'REQUEST_METHOD') !== "POST") {
    header("Location: /");
    die();
}
if (!$_FILES['file']) {
    echo "missing required parameter file";
    die();
}
if ($_FILES['file']['size'] > 500000){
    echo "file is too large";
    die();
}

wh_log("file ".$_FILES["file"]["name"]." uploaded from ip ".$_SERVER['REMOTE_ADDR']);

$target_dir = "./files/";
$target_file = $target_dir . basename($_FILES["file"]["name"]);
move_uploaded_file($_FILES["file"]["tmp_name"], $target_file);
header("Location: ".$_SERVER["HTTP_BASE"]);
die();