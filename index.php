<!--
Rapsberry Pi Projects For Dummies: temperature log
For the Raspberry Pi
-->

<?php
include("dbreader.php");
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html> 

<head> 
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>index</title>
<meta http-equiv="imagetoolbar" content="false">

<style type="text/css">
<!--

a:link {color: #0000ff;}
a:visited {color: #800080;}
a:active {color: #ff0000;}

body {
  margin: 0;
  height: 100%;
  width: 100%;
  text-align: center;
  background-color: #ffffff;
}
img {
  border-width: 0;
  vertical-align: top;
}
.dfltc {
  font-family: 'Times New Roman';
  font-size: 12px;
  font-weight: normal;
  font-style: normal;
  text-decoration: none;
  text-align: left;
  color: #000000;
}

#centered {
  position: relative;
  width: 640px;
  height: 100%;
  margin: 0px auto 0 auto;
  text-align: left;
  padding-left: 1px;
  cursor: default;
}
#Oobj10 {
  position: absolute;
  font-size: 10px;
  z-index: 1;
  left: 0.00em;
  top: 0.00em;
  width: 64.00em;
  height: 69.10em;
}
img#Ggeo18 {
  width: 100%;
  height: 100%;
}
#Oobj11 {
  position: absolute;
  font-size: 10px;
  z-index: 3;
  text-align: left;
  left: 8.90em;
  top: 40.30em;
  width: 28.70em;
  height: 19.80em;
}
#Oobj16 {
  position: absolute;
  font-size: 10px;
  z-index: 5;
  text-align: left;
  left: 26.10em;
  top: 26.80em;
  width: 9.30em;
  height: 4.40em;
}

.temperature {
  position: relative;
  font-family: 'Arial Unicode MS', sans-serif;
  font-size: 32px;
  color: black;
  text-align:left;
}

tr:nth-child(odd) {background: #F7F772}

td { 
    padding: 0px 60px 0px 60px;
}

.temperature_table {
  position: relative;
  font-family: 'Arial Unicode MS', sans-serif;
  font-size: 16px;
  color: black;
  text-align:center;
}

.temperature_div {
  width:470px; 
  height:200px; 
  overflow:auto;
}

-->
</style>
</head> 

<body>

<div id="centered">
<div id="Oobj10">
<img id="Ggeo18" src="RPIPFDTLBanner.png" alt="">
</div>

<div id="Oobj11">
<div id="Gcode46" class="dfltc">
<?php
DisplayTemperatureLog(100);?></div>
</div>

<div id="Oobj16">
<div id="Gcode54" class="dfltc">
<?php
DisplayLatestTemperature();
?></div>
</div>


</div>
</body> 
</html> 
