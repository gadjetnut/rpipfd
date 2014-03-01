#!/usr/bin/env python
"""
Rapsberry Pi Projects For Dummies: temperature logger to PrivateEyePi
For the Raspberry Pi
"""

import time
import RPi.GPIO as GPIO
import urllib2
import subprocess
import globals
from alarmfunctionsr import UpdateHost
from alarmfunctionsr import GetDataFromHost
from alarmfunctionsr import SendEmailAlert
from ds18b20 import GetTemperature
                                 
def NotifyHostTemperature():
        numtemp = len(globals.DallasSensorNumbers)
        rt2=False
        for z in range(0,numtemp,1):
                TempBuffer = []
                temperature_reading = GetTemperature(globals.Farenheit, globals.DallasSensorDirectory[0]) 
                TempBuffer.append(temperature_reading)
                if globals.Farenheit:
                        TempBuffer.append(1)
                else:
                        TempBuffer.append(0)
                TempBuffer.append(globals.DallasSensorNumbers[z])
                UpdateHost(14, TempBuffer)
        return (0)
                   
def main():
        global start_temperature_time
        global elapsed_temperature_time
        
        globals.init()
        start_temperature_time = time.time()
        elapsed_temperature_time=9999
        
        #Main Loop
        while True:
                        
            if (elapsed_temperature_time > globals.TemperaturePollInterval):
                    start_temperature_time = time.time()
                    # Get the latest temperature
                    NotifyHostTemperature()
                    
            elapsed_temperature_time = time.time() - start_temperature_time
                
            time.sleep(.2)

if __name__ == "__main__":
        main()
