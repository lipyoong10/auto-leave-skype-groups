from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys 
from selenium import webdriver
from time import sleep
import os

def click_Button_by_xpath( driver, xpath ):
    xpathButton = driver.find_element_by_xpath( xpath )
    xpathButton.click()
    
# First, launch the web app and ask user to login
currentDirectory = os.getcwd()
chromeDriverLocation = os.path.join( currentDirectory, "chromedriver.exe" )
# - Setup ChromeDriver with incognito mode
options = webdriver.ChromeOptions()
options.add_argument("--incognito --start-maximized")
chromeDriver = webdriver.Chrome(options=options)

skypeURL = "https://web.skype.com/"

chromeDriver.get( skypeURL )

# Wait until "CHATS" pop up to begin
xPathGotItCustomizeYourProfileButton = '//*[@data-text-as-pseudo-element="Got it!"]'
temporaryTimeOut = 60
xPathGotItCustomizeYourProfileButton_present = EC.presence_of_element_located((By.XPATH, xPathGotItCustomizeYourProfileButton))
WebDriverWait( chromeDriver, temporaryTimeOut).until(xPathGotItCustomizeYourProfileButton_present)
sleep(1)
click_Button_by_xpath( chromeDriver, xPathGotItCustomizeYourProfileButton )

#If the above button exists, press it first
#sleep(30)   #Give it 30 seconds to load up all chats into the Web App 

xPathCHATStitle = '//*[@data-text-as-pseudo-element="CHATS"]'
#If the above CHAT title exists, after clicking "Got it!" Scroll down to collect all

xPathScrollbar = '//*[@aria-label="Conversations list"]//*[@class="slider"]'
xPathScrollbar_present = EC.presence_of_element_located((By.XPATH, xPathScrollbar))
WebDriverWait( chromeDriver, temporaryTimeOut).until(xPathScrollbar_present)
sleep(2)

participantButtonDefaultXPath = '/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div/div[2]/div/div[1]/div[1]/div/div[1]/div/div/div/div/div/button[1]'
leaveGroupDefaultXPath = '/html/body/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/div/div/div[2]/div[1]/div/div[3]/div[2]/div[7]/button/div[1]/div/div'
leaveGroupConfirmationXPath = '/html/body/div[1]/div/div[2]/div/div[3]/div/div/div[3]/button[2]/div'


currentNumber = int(0)   #Current guess - It seems like chat bubble starts from index 6
while True:
    currentNumberString = str(currentNumber)
    xPathChatIndex = '//*[@id="rx-vlv-' + currentNumberString + '"]'
    print(xPathChatIndex)
    try:
        element = chromeDriver.find_element_by_xpath( xPathChatIndex )
        actions = ActionChains(chromeDriver)
        actions.move_to_element(element).perform()
        sleep(1)

        click_Button_by_xpath( chromeDriver, xPathChatIndex)
        sleep(1)
        click_Button_by_xpath( chromeDriver, xPathChatIndex)
        sleep(1)

        chatShortTitle = chromeDriver.find_element_by_xpath( participantButtonDefaultXPath ).get_attribute('title')
        print(chatShortTitle)

        if "participant" in chatShortTitle:        
            click_Button_by_xpath( chromeDriver, participantButtonDefaultXPath )
            print('pressed {}'.format(chatShortTitle))

            element = chromeDriver.find_element_by_xpath( leaveGroupDefaultXPath )
            actions = ActionChains(chromeDriver)
            actions.move_to_element(element).perform()
            sleep(1)
            
            sleep(1)
            click_Button_by_xpath( chromeDriver, leaveGroupDefaultXPath )
            print('xpath pressed: {}'.format('Leave group button'))
            sleep(1)

            click_Button_by_xpath( chromeDriver, leaveGroupConfirmationXPath)
            print('pressed leave group confirmed button')
            sleep(1)

        
    except Exception:
        print("Couldn't find {}".format(xPathChatIndex))
        pass
    
    currentNumber += 1



xPathScrollbar = '//*[@aria-label="Conversations list"]//*[@class="slider"]'

xPathCHATgroups = '//*[@role="group" and @aria-label="CHATS"]'

# First, scroll down all the way to collect ALL Skype chats
# Click on the first CHATS group. For each CHATS group that has "participants" means that it is a Skype GROUP
# Type "/leave" and ENTER
# Repeat until all CHATS group are iterated 
