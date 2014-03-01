#!/usr/bin/env python
"""
globals.py 3.00 PrivateEyePi Globals Parameters
---------------------------------------------------------------------------------
 Works conjunction with host at www.privateeyepi.com                              
 Visit projects.privateeyepi.com for full details                                 
                                                                                  
 J. Evans October 2013       
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                                       
                                                                                  
 Revision History                                                                  
 V1.00 - Release
 V2.00 - Added generic poll interval
 V3.00 - Incorporated rules functionality
 V4.00 - Added siren rule action, chime, siren beep delay                                                             
 -----------------------------------------------------------------------------------
"""

def init():
        global PrintToScreen
        global user
        global password
        global RFPollInterval
        global smtp_server
        global smtp_user
        global smtp_pass
        global Farenheit
        global DallasSensorNumbers
        global DallasSensorDirectory
        global TemperaturePollInterval
        global GenericPollInterval
        global GPIOPollInterval
        global UseSiren
        global SirenGPIOPin
        global SirenTimeout
        global SirenStartTime
        global Armed
        global RemoteZoneDescription
        global ArmPin
        global DisarmPin
        global ArmDisarm
        global GPIO 
        global ChimeDuration
        global SirenPollInterval
        global SirenDelay
        global BeepDuringDelay
        global ButtonBList
        global ButtonBId
        global dht22_gpio
        global dht22_pin_no
        
        #User and password that has been registered on www.privateeyepi.com website
        user=""     #Enter email address here
        password="" #Enter password here
        
        # Set this to True if you want to send outputs to the screen
        # This is useful for debugging
        PrintToScreen=False
        
        # Interval in seconds that the alarm system polls the server for changes to zones and locations
        GPIOPollInterval=300
        
        #Poll Intervals in seconds for a RF sensor
        RFPollInterval=300
        
        # If you want to receive email alerts define SMTP email server details
        # This is the SMTP server, username and password trequired to send email through your internet service provider
        smtp_server=""	# usually something like smtp.yourisp.com
        smtp_user=""    	    # usually the main email address of the account holder
        smtp_pass="" 		        # usually your email address password
        
        #Indicator to record temperature in Farenheit
        Farenheit=False
        
        #Temperature poll interval in seconds
        TemperaturePollInterval=300
                
        #Temperature settings
        #if you are using the dht22 temperature and humidity sensor set the gpio number and the pin number here
        # note!! the GPIO number and the pin number are not the same e.g GPIO4=RPIPin7
        dht22_gpio=4
        dht22_pin_no=7
        
        DallasSensorNumbers = []
        DallasSensorDirectory = []
        
        #Set the directory and sensor numbers for the Dallas temperature gauge
        DallasSensorNumbers.append(7) #sensor number defined in the number field in the GPIO settings
        #DallasSensorNumbers.append(80) #add more sensors..
        #DallasSensorNumbers.append() #add more sensors..
        
        DallasSensorDirectory.append("28-0000055d57dd") #directory name on RPI in the /sys/bus/w1/devices directory 
        #DallasSensorDirectory.append("28-000005020815") #add another directory 
        #DallasSensorDirectory.append("") #add another directory

        #Generic poll interval in seconds
        GenericPollInterval=300
        
        # Set this to true if you want to connect an external siren. Put siren activation and deactivation code in the Siren function.
        UseSiren = False
        SirenGPIOPin = 18
        SirenDelay=30 #The amount of time the siren will delay before it sounds
        BeepDuringDelay = True #if your want the siren to beep during the SirenDelay period
        SirenTimeout = 30 #siren will timeout after 30 seconds
        ChimeDuration = 5

        # Poll interval to check server for siren deactivation
        SirenPollInterval=5
        
        #Arm/Disarm zone from a switch
        ArmDisarm=False # set this to True if you want to arm/disarm using switches
        RemoteZoneDescription="" #The description of the zone you want to arm/disarm
        ArmPin=13
        DisarmPin=15
        Armed = False

        #Configure your button B sensors here
        #Button B is the second button on the RF Switch
        ButtonBList = []
        ButtonBId = []
        #ButtonBList.append(80) # this is the device ID of the sensor 
        #ButtonBId.append(90)   # sensor number defined in the number field in the GPIO settings
        
        #ButtonBList.append(81)
        #ButtonBId.append(90)
        #...add more button B sensors by copying the above two lines and updating the numbers in brackets....
        
        
