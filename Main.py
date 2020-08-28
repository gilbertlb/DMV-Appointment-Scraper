'''
Created on Jul 20, 2020

@author: Landon Gilbert
'''
import Main_Ping
import time

foundAppointment = False

# Activates the script every 5 minutes that a suitable appointment hasn't been found
# Upon confirmation of an appointment, the cycle will end until restarted by a user
time.sleep(10)
while not foundAppointment:
    foundAppointment = Main_Ping.main()
    if not foundAppointment:
        time.sleep(300)