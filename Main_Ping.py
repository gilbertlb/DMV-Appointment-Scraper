'''
Created on Jul 20, 2020

@author: Landon Gilbert
'''

from selenium import webdriver
from selenium.webdriver.support.select import Select
import csv
import time 
 
# Used to contain the process of filling out the appointment form 
def makeAppointment( driver, firstName, lastName, phoneNum, emailAddr ):
    
    # Attempt to fill out the form with the information taken from info.csv
    # If the attempt happens with no exceptions, it returns true, if an issue occurs it returns false
    try:
        driver.find_element_by_name("firstName").send_keys( firstName )
        driver.find_element_by_name("lastName").send_keys( lastName )
        driver.find_element_by_name("phone").send_keys( phoneNum )
        driver.find_element_by_name("email").send_keys( emailAddr )
        driver.find_element_by_xpath("/html/body/div[2]/form/div[4]/div[3]/div/div/input").click()
        time.sleep(10)
        return True
    except:
        return False

def main():
    time.sleep(5)
    infoFile = open("info.csv", "r")
    info = csv.reader(infoFile, delimiter=",").next()
    locationsFile = open("locations.csv", "r")
    locations = csv.reader(locationsFile, delimiter=',')
    
    opt = webdriver.ChromeOptions()
    #opt.add_argument('headless')
    
    driver = webdriver.Chrome(options=opt)
    
    for row in locations:
        if len(row) == 0:
            break
        
        print("Checking: " + row[1])
        
        driver.get( row[0] )
        driver.implicitly_wait(5)
        
        # Click the button for the non-testing license
        driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/div[2]/div[1]/label[1]").click()
        driver.implicitly_wait(1)
        driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/div[2]/div[2]/div[3]/div[1]").click()
        driver.implicitly_wait(1)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 150)")
        time.sleep(1)
        
        try:
            curElem = driver.find_element_by_class_name("no-dates-available")
        except: 
                # Select the calendar to determine the month  
                curElem = Select( driver.find_element_by_id("chooseMonthSched") )
                month = curElem.first_selected_option.get_attribute('value')
                month = int(month[5]+month[6])
                
                # Determine if the month matches the desired month
                if (int(month) == int(info[0])):
                    print("    Current location has the desired month open")
                    # If it does, retrieve the days available
                    dayList = driver.find_elements_by_xpath("//*[@id='step-pick-appointment']/div[2]/div[4]/div[1]/table[2]/tbody/tr/td[@class='scheduleday  activeday']")
                    # Check if the day was successfully retrieved, if not abort this page
                    if (len(dayList) == 0):
                        continue
                    # If the days are valid, determine if the earliest is before the given cutoff, if so make an appointment at the earliest time
                    else:
                        day = dayList[0].get_attribute('day')
                        day = int(day[8] + day[9])
                        
                        # If the day falls before the cut-off given by info.csv
                        if day < int(info[1]):
                            print("    Current location has one or more days open within the cutoff given")
                            dayList[0].click()
                            driver.find_elements_by_xpath("//*[@role='radio']")[0].click()

                            # Due to a quirk with the page, the continue button must be clicked twice to use it
                            try:
                                driver.find_element_by_partial_link_text("Continue").click()
                            except:
                                driver.find_element_by_partial_link_text("Continue").click()
                            
                            # If an appointment is made without issue, return True for main, otherwise continue searching
                            if makeAppointment( driver, info[2], info[3], info[4], info[5]):
                                print("    An appointment has been made at " + row[1])
                                return True
    locationsFile.close()
    # If no appointments are made for any page, return False and try again in five minutes
    return False
    