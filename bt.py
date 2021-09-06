
from selenium import webdriver
from time import sleep
import time

def getDelay(actionbutton,XPathList,XPathBases,driver):
	try :
		delayString = driver.find_element_by_xpath(XPathBases[actionbutton]+XPathList["delayXPath"]).text
		print(delayString)
		st = delayString.replace("Please wait ","")
		st = st.replace(" for your next submit!","")
		struct_time = time.strptime(st, "%M minute(s) %S seconds")
		return struct_time.tm_min*60+struct_time.tm_sec+5
	except:
		return -1
def mainPageSelect(XPathList,driver,action):
	try:
		driver.find_element_by_xpath(XPathList[action]).click()
	except:
		print("You didn't solve the captcha")
		driver.refresh()
def executionSteps(XPathList,XPathBases,driver,vidURL,action,actionbutton):
	try:
		sleep(2)
		driver.find_element_by_xpath(XPathBases[actionbutton]+XPathList["urlinputBox"]).clear()
		driver.find_element_by_xpath(XPathBases[actionbutton]+XPathList["urlinputBox"]).send_keys(vidURL)
		sleep(1)
		driver.find_element_by_xpath(XPathBases[actionbutton]+XPathList["searchButton"]).click()
		sleep(2)
		increaseString = driver.find_element_by_xpath(XPathBases[actionbutton]+XPathList["executeButton"]).text
		driver.find_element_by_xpath(XPathBases[actionbutton]+XPathList["executeButton"]).click()
		sleep(5)
		print(f"Delivering {increaseString} {action}")
	except:
		delay = getDelay(actionbutton,XPathList,XPathBases,driver)
		print(f"Delay:{delay}\tA generic error occurred. Now will retry again")
		if delay != -1:
			sleep(delay)
		driver.refresh()
		sleep(2)

def loop(action,actionbutton,XPathList,XPathBases,vidURLs,driver,defaultwait=360,loops=10):
	count = 0
	while count != loops:
		vidnum = count % len(vidURLs)
		mainPageSelect(XPathList,driver,actionbutton)

		executionSteps(XPathList,XPathBases,driver,vidUrls[vidnum],action,actionbutton)
		sleep(5)


		try:
			delay = getDelay(actionbutton,XPathList,XPathBases,driver)
			print(f"Delay is {delay}\n")
			if delay == -1:
				driver.refresh()
				continue
			elif delay > defaultwait:
				sleep(delay)
			else:
				sleep(defaultwait)

		except:
			print("action didnt work")
	count+=1
XPathList = {
	# 1. main page actions after captcha page
	"followersButton":"/html/body/div[4]/div[1]/div[3]/div/div[1]/div/button",
	"heartsButton":"/html/body/div[4]/div[1]/div[3]/div/div[2]/div/button",
	"commentsHeartsButton":"/html/body/div[4]/div[1]/div[3]/div/div[3]/div/button",
	"viewsButton":"/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button",
	"sharesButton":"/html/body/div[4]/div[1]/div[3]/div/div[5]/div/button",
	"livestreamButton":"/html/body/div[4]/div[1]/div[3]/div/div[6]/div/button",
	# 2. after selecting an action this button appears
	"urlinputBox":"/div/form/div/input",
	"searchButton":"/div/form/div/div/button",
	# 3. after pressing search button this button appears telling you how many actions are available
	"executeButton":"/div/div/div[1]/div/form/button",# Button Text contains number to send
	# 4. this appears after sending the actions 
	"delayXPath":"/div/div/h4", # should contain a number followed by "minute(s)"
	"successText":"/div/div/span" # Should contain Successfully if it was successful
}
XPathBases = {
		"followersButton":"",
		"heartsButton":"/html/body/div[4]/div[3]",
		"commentsHeartsButton":"/html/body/div[4]/div[4]",
		"viewsButton":"/html/body/div[4]/div[5]",
		"sharesButton":"/html/body/div[4]/div[6]",
		"livestreamButton":"/html/body/div[4]/div[7]",
}
vidUrls = [
	"https://www.tiktok.com/@/video/",	# Change to video URL and add more if needed
]

bot = int(input("What do you want to do?\n1 - Auto views(500)\n2 - Auto hearts\n3 - Auto (FIRST) comments heart\n4 - Auto followers\n5 - Auto Share\n6 - Live Stream\n"))
i = 0

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument(f'--window-size={480},{480}')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path=r'PATH/TO/chromedriver',chrome_options=chrome_options) #Change path to your own path

driver.get("https://vipto.de/")
input("Hit Enter After entering captcha\n")

if bot == 1:
    loop("Views","viewsButton",XPathList,XPathBases,vidUrls,driver)
elif bot == 2:
    loop("Hearts","heartsButton",XPathList,XPathBases,vidUrls,driver)
elif bot == 3:
    loop("Comment Hearts","commentsHeartsButton",XPathList,XPathBases,vidUrls,driver)
elif bot == 4:
    loop("Followers","followersButton",XPathList,XPathBases,vidUrls,driver)
elif bot == 5:
    loop("Shares","sharesButton",XPathList,XPathBases,vidUrls,driver)
elif bot == 6:
    loop("Live Stream","livestreamButton",XPathList,XPathBases,vidUrls,driver)
else:
    print("You can insert just 1, 2, 3, 4, 5 or 6")
