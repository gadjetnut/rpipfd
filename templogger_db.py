#!/usr/bin/env python
"""
Rapsberry Pi Projects For Dummies: temperature database logger
For the Raspberry Pi
"""
import subprocess 
import time
import MySQLdb
from ds18b20 import GetTemperature

directory = "28-00000586acff"

def main():
        # This is the main routine of the program
        
        # set how long to wait between logs
        poll_interval = 5
        
        # set the following variable to true if you 
        #want to log in Fahreheit
        fahrenheit=True
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
                        rt = GetTemperature(fahrenheit, directory)
                        if (rt=="error"):
                                #reset the timer and try again 
                                #after the 5 min delay
                                start_time = time.time()
                                continue
                            
                        temperature=rt
                        
                        # log the temperature to the database
                        # open database connection
                        db = MySQLdb.connect("localhost","dblogger","password","sensor_logs" )
                        
                        # prepare a cursor object using cursor() 
                        # method
                        cursor = db.cursor()
                        
                        # build the SQL statement
                        sql = "INSERT INTO temperature_log (temperature, date, unit_of_measure) VALUES (%d, NOW(), '%c')" % (temperature, unit_of_measure)  
                        
                        # Execute the SQL command
                        cursor.execute(sql)
                        
                        # Commit your changes in the database
                        db.commit()
                        
                        # disconnect from server
                        db.close()
                        
                        print "Temperature of "+\
                        str(temperature)+unit_of_measure+" logged"
                        
                        # reset the timer
                        timer = time.time()  
                time.sleep(.2)

if __name__ == "__main__":
        main()
