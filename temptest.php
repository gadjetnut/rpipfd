<!--
Rapsberry Pi Projects For Dummies: test program to display the temperature log
For the Raspberry Pi
-->

<?php
    include ("dbreader.php");
    echo "The current temperature is:";
    echo DisplayLatestTemperature();
    echo "The last 10 temperature logs are:";
    echo DisplayTemperatureLog(10);
?>
