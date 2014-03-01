#!/usr/bin/env python
"""
Rapsberry Pi Projects For Dummies: temperature logger to google docs spreadsheet
For the Raspberry Pi
"""
import subprocess 
import time
from ds18b20 import GetTemperature
from gdocs import LogRowInGDocSpreadsheet

ds18b20_dir     = ""
client_id       = ""
client_secret   = ""
spreadsheet_key = ""
fahrenheit      = True
headings = ["Temperature", "Date", "Unit"] #column headings can't have spaces

def main():
        # This is the main routine of the program
        
        # set how long to wait between logs
        poll_interval = 5
        
        if fahrenheit:
                unit_of_measure = 'F'
        else:
                unit_of_measure = 'C'
                
        # Get the start time 
        timer = time.time() - poll_interval
        
        # main loop forever
        while (True):
                #log the temperature every X seconds
                if time.time() - timer > poll_interval: 
                        # get the latest temperature from 
                        #the sensor
                        rt = GetTemperature(fahrenheit, ds18b20_dir)
                        if (rt=="error"):
                                #reset the timer and try again 
                                #after the 5 min delay
                                start_time = time.time()
                                continue
                            
                        temperature=rt
                        
                        #Send the temperature reading to Google Docs
                        LogRowInGDocSpreadsheet(client_id, client_secret, spreadsheet_key, headings, temperature, unit_of_measure);
                                                
                        print "Temperature of "+\
                        str(temperature)+unit_of_measure+" logged"
                        
                        # reset the timer
                        timer = time.time()  
                time.sleep(.2)

if __name__ == "__main__":
        main()

