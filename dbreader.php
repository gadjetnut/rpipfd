<!--
Rapsberry Pi Projects For Dummies: PHP functions that read from the temperature log
For the Raspberry Pi
-->

<?php
function DisplayTemperatureLog($num_rows_to_display){
    $mysqli = new mysqli("localhost", 
                         "dblogger", 
                         "password", 
                         "sensor_logs");

    if ($mysqli->connect_errno) {
        echo "Failed to connect to MySQL: (" . 
        $mysqli->connect_errno . 
             ") " . $mysqli->connect_error;
    }
    $sql = "SELECT * FROM temperature_log ORDER BY date DESC";
    $res = $mysqli->query($sql);
    if (!$res) {
        echo "Table query failed: (" . 
        $mysqli->errno . 
        ") " . $mysqli->error;
    }

    if ($res->num_rows==0)
        {
        echo "No data in log";	
        return(0);
        }
    
    echo "<div class='temperature_div'>";
    echo "<table class='temperature_table'>";
    echo "<tr>";
    echo "<th>Date</th>";
    echo "<th>Temperature</th>";
    echo "</tr>";
    
    for ($row_no = 0; 
         $row_no < $res->num_rows && $row_no < $num_rows_to_display; 
         $row_no++) {
        echo "<tr>";
        $res->data_seek($row_no);
        $row = $res->fetch_assoc();
        echo "<td>".$row['date']."</td>";
        echo "<td>".$row['temperature']."&deg;".
        $row['unit_of_measure']."</td>";
        echo "</tr>";
    }
    echo "</table>";
    echo "</DIV>";
}

function DisplayLatestTemperature(){
    $mysqli = new mysqli("localhost", 
                         "dblogger", 
                         "password", 
                         "sensor_logs");
    if ($mysqli->connect_errno) {
        echo "Failed to connect to MySQL: (" . 
        $mysqli->connect_errno . ") " . 
        $mysqli->connect_error;
    }
    
    $sql = "SELECT * FROM temperature_log ORDER BY date DESC limit 1";
    $res = $mysqli->query($sql);
    if (!$res) {
        echo "Table query failed: (" . 
        $mysqli->errno . ") " . $mysqli->error;
    }
    
    if ($res->num_rows==0)
        {
        echo "No data in log";	
        return(0);
        }
        
    $res->data_seek(0);
    $row = $res->fetch_assoc();
    echo "<DIV class='temperature'>".
    $row['temperature']."&deg;".
    $row['unit_of_measure']."</DIV>";
}

?>
