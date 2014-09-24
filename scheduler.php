<?
# Write data to a temp file
$data = $_POST["txt"];
$tmpfname = tempnam("/tmp", "interviewscheduler");
$handle = fopen($tmpfname, "w");
fwrite($handle, $data);
fclose($handle);

# Run scheduler
$cmd = "./scheduler-max-flow-web.py " . $tmpfname;
$output = `$cmd`;
echo $output;

# Delete temp file
`rm $tmpfname`;
?>
