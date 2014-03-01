#!/usr/bin/env python
"""
Rapsberry Pi Projects For Dummies: DS18B20 temperature sensor routines
For the Raspberry Pi
"""
import time
import subprocess

def fileexists(filename):
        try:
                with open(filename): pass
        except IOError:
                return False
        return True

def GetTemperature(fahrenheit, directory):
        
        #Read the sensor 5 times checking the CRC 
        #until we have a good read 
        for retries in range(0, 5):
                #These two lines call the modprobe
                #application to get the temperature 
                #from the sensor
                subprocess.call(['modprobe', 'w1-gpio'])
                subprocess.call(['modprobe', 'w1-therm'])
                
                #Open the file that you viewed earlier so that
                #Python can see what is in it. Replace the 
                #serial number with your own number
                filename = "/sys/bus/w1/devices/"+directory+"/w1_slave"
                if (fileexists(filename)):
                        tfile = open(filename)
                else:
                        return "error"
                # Read the w1_slave file into memory
                text = tfile.read()
                # Close the file
                tfile.close()
                #Perform a CRC Check to prevent us logging
                #bad reads
                firstline  = text.split("\n")[0]
                crc_check = text.split("crc=")[1]
                crc_check = crc_check.split(" ")[1]
                if crc_check.find("YES")>=0:
                        break
        
        #If after 5 tries you were unable to get a good read
        #then fail
        if retries==5:
                return "error"
            
        # You are interested in the second line so this code will  
        # put the second line into the secondline variable
        secondline = text.split("\n")[1]
        # You are interested in the 10th word on the second line
        temperaturedata = secondline.split(" ")[9]
        # You are interested in the number of the 10 word so 
        # you discard the first two letters "t=" and convert 
        # the remaining number $
        temperature = float(temperaturedata[2:])
        # Divide the value by 1000 to get the decimal in the 
        # right place
        temperature = temperature / 1000
        temp = float(temperature)
        # Do the Farenheit conversion if required
        if fahrenheit:
                temp=temp*1.8+32
        temp = round(temp,2)
        return(temp)

