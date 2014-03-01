#!/usr/bin/env python
"""
alarmfunctionsr.py 2.00 PrivateEyePi Common Functions
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
 V2.00 - Incorporation of rules functionality                                                             
 -----------------------------------------------------------------------------------
"""

import globals
import urllib2
import smtplib
import time
import sys
import thread
import RPi.GPIO as GPIO
from email.mime.text import MIMEText
    
def find_all(a_str, sub):
        start = 0
        cnt=0
        while True:
                start = a_str.find(sub, start)
                if start == -1: 
                        return cnt
                start += len(sub)
                cnt=cnt+1
        
def isNumber(x):
        # Test whether the contents of a string is a number
        try:
                val = int(x)
        except ValueError:
                return False
        return True


def UpdateHostThread(function,opcode):
        try:
                thread.start_new_thread(UpdateHostThread, (function,opcode, ) )
        except:
                print "Error: unable to start thread"

def UpdateHost(function,opcode):
        # Sends data to the server 
        script_path = "https://www.privateeyepi.com/rules/beta/alarmhostr.php?u="+globals.user+"&p="+globals.password+"&function="+str(function)
        
        i=0
        for x in opcode:
            	script_path=script_path+"&opcode"+str(i)+"="+str(opcode[i])
            	i=i+1
        
        if globals.PrintToScreen: print "Host Update: "+script_path 
        try:
                rt=urllib2.urlopen(script_path)
        except urllib2.HTTPError:
            	if globals.PrintToScreen: print "HTTP Error"
            	return False
        time.sleep(.2)
        temp=rt.read()
        if globals.PrintToScreen: print temp
        l = find_all(temp,"/n");
        RecordSet = temp.split(',')
        c=[]
        y=0
        c.append([])
        for x in RecordSet:
                if x=="/n":
                        y=y+1
                        if y < l:
                                c.append([])
                else:
                        if isNumber(x):
                                c[y].append(int(x))
                        else:
                                c[y].append(x)
        rt=ProcessActions(c)
        if rt==False:
                return(False)
        else:
            return(c)

def ProcessActions(ActionList):
        FalseInd=True
        for x in ActionList:
            if x[0]=="/EMAIL":
                    SendEmailAlertFromRule(x[1], x[2])
                    x.remove
            if x[0]=="/CHIME":
                    StartChimeThread()
                    x.remove
            if x[0]=="/rn588":
                    exit()
            if x[0]=="/FALSE":
                    FalseInd=False
            if x[0]=="/SIREN":
                    StartSirenThread(x[2])
                    x.remove
        return(FalseInd)

def StartSirenThread(Zone):
        try:
                thread.start_new_thread(Siren, (Zone, ) )
        except:
                print "Error: unable to start thread"

def Siren(Zone):
        GPIO.setmode(GPIO.BOARD)
        if globals.UseSiren == True:
                GPIO.setup(globals.SirenGPIOPin, GPIO.OUT) #Siren pin setup
        else:
                return
        
        if globals.SirenDelay>0:
                globals.SirenStartTime = time.time()
                while time.time() < globals.SirenStartTime + globals.SirenDelay:
                        if globals.BeepDuringDelay:
                                GPIO.output(globals.SirenGPIOPin,True)
                                time.sleep(1)
                                GPIO.output(globals.SirenGPIOPin,False)
                                time.sleep(4)
        
        GPIO.output(globals.SirenGPIOPin,True)
        globals.SirenStartTime = time.time()
        if globals.PrintToScreen: print "Siren Activated"
        while time.time() < globals.SirenStartTime + globals.SirenTimeout:
                time.sleep(globals.SirenPollInterval)
                if CheckForSirenDeactivation(Zone) == True:
                        break
        GPIO.output(globals.SirenGPIOPin,False)
        if globals.PrintToScreen: print "Siren Deactivated"
    
def CheckForSirenDeactivation(Zone):
        # Routine to fetch the location and zone descriptions from the server 
        RecordSet = GetDataFromHost(16,[Zone])
        if globals.PrintToScreen: print RecordSet
        ZoneStatus=RecordSet[0][0]
        if ZoneStatus=="FALSE":
                return (True)    

def StartChimeThread():
        try:
                thread.start_new_thread(SoundChime, ())
        except:
                print "Error: unable to start thread"

def SoundChime():
        if globals.ChimeDuration>0:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(globals.SirenGPIOPin, GPIO.OUT) #Siren pin setup
                GPIO.output(globals.SirenGPIOPin,True)
                time.sleep(globals.ChimeDuration)
                GPIO.output(globals.SirenGPIOPin,False)
                    
def GetDataFromHost(function,opcode):
# Request data and receive reply (request/reply) from the server
 
        script_path = "https://www.privateeyepi.com/rules/beta/alarmhostr.php?u="+globals.user+"&p="+globals.password+"&function="+str(function)
        
        i=0
        for x in opcode:
                script_path=script_path+"&opcode"+str(i)+"="+str(opcode[i])
                i=i+1
            
        if globals.PrintToScreen: print script_path 
        try:
                rt = urllib2.urlopen(script_path)
        except urllib2.HTTPError:
                return False
        temp=rt.read()
        if globals.PrintToScreen: print temp
        
        l = find_all(temp,"/n");
        RecordSet = temp.split(',')
        c=[]
        y=0
        c.append([])
        for x in RecordSet:
                if x=="/n":
                        y=y+1
                        if y < l:
                                c.append([])
                else:
                        if isNumber(x):
                                c[y].append(int(x))
                        else:
                                c[y].append(x)
        rt=ProcessActions(c)   
        if rt==False:
                return(False)
        else:
            return(c) 
        return(c)

def BuildMessage(SensorNumber):
        # Routine to fetch the location and zone descriptions from the server  
        
        RecordSet = GetDataFromHost(6,[SensorNumber])
        if globals.PrintToScreen: print RecordSet
        if RecordSet==False:
                return  
        zonedesc=RecordSet[0][0]
        locationdesc = RecordSet[0][1]
        messagestr="This is an automated email from your house alarm system. Alarm activated for Zone: "+zonedesc+" ("+locationdesc+")"
        return messagestr

def BuildMessageFromRule(SensorNumber, smartruleid):
        
    RecordSet = GetDataFromHost(7,[smartruleid, SensorNumber])
    if RecordSet==False:
        return

    numrows = len(RecordSet)  

    messagestr="This is an automated email from PrivateEyePi. Rule triggered for Zone(s): "+RecordSet[0][3]+", Location: "+RecordSet[0][4]+" and for rule "
    for i in range(0,numrows,1):
        if RecordSet[i][0]==1:
            messagestr=messagestr+"Alarm Activated"
        if RecordSet[i][0]==2:
            messagestr=messagestr+"Alarm Deactivated"
        if RecordSet[i][0]==3:
            messagestr=messagestr+"Circuit Open"
        if RecordSet[i][0]==4:
            messagestr=messagestr+"Circuit Closed"
        if RecordSet[i][0]==5:
            messagestr=messagestr+"Open for " + str(RecordSet[i][1]) + " Minutes"
        if RecordSet[i][0]==6:
            messagestr=messagestr+"Closed for " + str(RecordSet[i][1]) + " Minutes"
        if RecordSet[i][0]==7:
            messagestr=messagestr+"Where sensor value (" + str(RecordSet[i][5]) + ") is between " + str(RecordSet[i][1]) + " " + str(RecordSet[i][2])            
        if RecordSet[i][0]==8:
            messagestr=messagestr+"Tamper"
        if RecordSet[i][0]==9:
            messagestr=messagestr+"Day Of Week is between " + str(RecordSet[i][1]) + " and " + str(RecordSet[i][2]) 
        if RecordSet[i][0]==10:
            messagestr=messagestr+"Hour Of Day is between " + str(RecordSet[i][1]) + " and " + str(RecordSet[i][2])
        if RecordSet[i][0]==11:
            messagestr=messagestr+"SmartAlert"
        if i<numrows-1:
            messagestr=messagestr + " AND "    
    return messagestr

def SendEmailAlertFromRule(ruleid, SensorNumber):
        try:
                thread.start_new_thread(SendEmailAlertThread, (SensorNumber, ruleid, True, ) )
        except:
                print "Error: unable to start thread"

def SendEmailAlert(SensorNumber):
        try:
                thread.start_new_thread(SendEmailAlertThread, (SensorNumber,0 , False, ) )
        except:
                print "Error: unable to start thread"

def SendEmailAlertThread(SensorNumber, smartruleid, ruleind):
    
        # Get the email addresses that you configured on the server
        RecordSet = GetDataFromHost(5,[0])
        if RecordSet==False:
                return
        
        numrows = len(RecordSet)
        
        if globals.smtp_server=="":
                return
        
        if ruleind:
                msg = MIMEText(BuildMessageFromRule(SensorNumber, smartruleid))
        else:
                msg = MIMEText(BuildMessage(SensorNumber))
                
        for i in range(numrows):
                # Define email addresses to use
                addr_to   = RecordSet[i][0]
                addr_from = globals.smtp_user #Or change to another valid email recognized under your account by your ISP      
                # Construct email
                msg['To'] = addr_to
                msg['From'] = addr_from
                msg['Subject'] = 'Alarm Notification' #Configure to whatever subject line you want
                
                # Send the message via an SMTP server
                s = smtplib.SMTP(globals.smtp_server)
                s.login(globals.smtp_user,globals.smtp_pass)
                s.sendmail(addr_from, addr_to, msg.as_string())
                s.quit()
                if globals.PrintToScreen: print msg;

def SendCustomEmail(msgText, msgSubject):
    
        # Get the email addresses that you configured on the server
        RecordSet = GetDataFromHost(5,[0])
        if RecordSet==False:
                return
        
        numrows = len(RecordSet)
        
        if globals.smtp_server=="":
                return
                
        for i in range(numrows):
                # Define email addresses to use
                addr_to   = RecordSet[i][0]
                addr_from = globals.smtp_user #Or change to another valid email recognized under your account by your ISP      
                # Construct email
                msg = MIMEText(msgText)
                msg['To'] = addr_to
                msg['From'] = addr_from
                msg['Subject'] = msgSubject #Configure to whatever subject line you want
                
                # Send the message via an SMTP server
                s = smtplib.SMTP(globals.smtp_server)
                s.login(globals.smtp_user,globals.smtp_pass)
                s.sendmail(addr_from, addr_to, msg.as_string())
                s.quit()
                if globals.PrintToScreen: print msg;

