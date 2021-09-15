
from selenium import webdriver
from time import sleep
import time
import pathlib
import json


class tiktokBoost():
	def __init__(self, vidURLS=[], serviceURL="", chromePath=""):
		self.AvailableActions = {
			"followersButton": True,
			"heartsButton": True,
			"commentsHeartsButton": True,
			"viewsButton": True,
			"sharesButton": True,
			"livestreamButton": True,
		}
		self.XPathMain = {
			# 1. main page actions after captcha page
			"followersButton": "/html/body/div[4]/div[1]/div[3]/div/div[1]/div/button",
			"heartsButton": "/html/body/div[4]/div[1]/div[3]/div/div[2]/div/button",
			"commentsHeartsButton": "/html/body/div[4]/div[1]/div[3]/div/div[3]/div/button",
			"viewsButton": "/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button",
			"sharesButton": "/html/body/div[4]/div[1]/div[3]/div/div[5]/div/button",
			"livestreamButton": "/html/body/div[4]/div[1]/div[3]/div/div[6]/div/button",
		}
		self.XPathList = {
			# 2. after selecting an action this button appears
			"urlinputBox": "/div/form/div/input",
			"searchButton": "/div/form/div/div/button",
			# 3. after pressing search button this button appears telling you how many actions are available
			# Button Text contains number to send
			"executeButton": "/div/div/div[1]/div/form/button",
			# 4. this appears after sending the actions
			# should contain a number followed by "minute(s)"
			"delayXPath": "/div/div/h4",
			"successText": "/div/div/span"  # Should contain Successfully if it was successful
		}
		self.XPathBases = {
			"followersButton": "/html/body/div[4]/div[2]",
			"heartsButton": "/html/body/div[4]/div[3]",
			"commentsHeartsButton": "/html/body/div[4]/div[4]",
			"viewsButton": "/html/body/div[4]/div[5]",
			"sharesButton": "/html/body/div[4]/div[6]",
			"livestreamButton": "/html/body/div[4]/div[7]",
		}
		if len(vidURLS) != 0:
			self.vidURLS = vidURLS
		else:
			print("List of vidURLS cannot be empty")
			exit()
		chrome_options = webdriver.ChromeOptions()
		# chrome_options.add_argument('--headless')
		chrome_options.add_argument(
			"--disable-blink-features=AutomationControlled")
		# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
		chrome_options.add_experimental_option(
			"excludeSwitches", ["enable-automation"])
		chrome_options.add_experimental_option('useAutomationExtension', False)
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument(f'--window-size={480},{480}')
		chrome_options.add_argument('--disable-dev-shm-usage')
		chrome_options.add_argument(
			'--ignore_local_proxy_environment_variables')
		# driver = webdriver.Chrome(executable_path=r'D:\PATH\geckodriver\bin\chromedriver',chrome_options=chrome_options) #Change it
		if chromePath != "":
			self.driver = webdriver.Chrome(
				executable_path=chromePath, options=chrome_options)  # Change it
		else:
			print("ChromePath cannot be empty")
		if serviceURL != "":
			self.driver.get(serviceURL)
		else:
			print("serviceURL cannot be empty")
		input("Hit Enter After entering captcha\n")
		sleep(3)
		self.checkAvailableActions()

	def countDown(self, mx):
		print("")
		for x in range(0, mx, 5):
			sleep(5)
			print(f"Wait {mx-x}---", end='\r')

	def checkAvailableActions(self):
		print("Checking list of available options")
		for a, x in self.XPathMain.items():
			try:
				btn = self.driver.find_element_by_xpath(x)
				if btn.get_attribute('disabled'):
					print(f"Action {a} not available\n")
					self.AvailableActions[a] = False
			except:
				print(f"Action {a} available\n")
				continue

	def getDelay(self, actionbutton):
		"Please wait 4 minute(s) 35 seconds for your next submit!"
		try:
			delayString = self.driver.find_element_by_xpath(
				self.XPathBases[actionbutton]+self.XPathList["delayXPath"]).text
			print(delayString)
			st = delayString.replace("Please wait ", "")
			st = st.replace(" for your next submit!", "")
			struct_time = time.strptime(st, "%M minute(s) %S seconds")
			return struct_time.tm_min*60+struct_time.tm_sec+5
		except:
			return -1

	def mainPageSelect(self, action):
		try:
			self.driver.find_element_by_xpath(self.XPathMain[action]).click()
		except:
			print("You didn't solve the captcha")
			self.driver.refresh()
			self.mainPageSelect(action)

	def executionSteps(self, vidURL, action, actionbutton):
		try:
			sleep(2)
			self.driver.find_element_by_xpath(
				self.XPathBases[actionbutton]+self.XPathList["urlinputBox"]).clear()
			sleep(2)
			self.driver.find_element_by_xpath(
				self.XPathBases[actionbutton]+self.XPathList["urlinputBox"]).send_keys(vidURL)
			sleep(2)
			self.driver.find_element_by_xpath(
				self.XPathBases[actionbutton]+self.XPathList["searchButton"]).click()
			sleep(2)
			increaseString = self.driver.find_element_by_xpath(
				self.XPathBases[actionbutton]+self.XPathList["executeButton"]).text
			sleep(2)
			self.driver.find_element_by_xpath(
				self.XPathBases[actionbutton]+self.XPathList["executeButton"]).click()
			sleep(5)
			print(f"Delivering {increaseString} {action}")
		except:
			delay = self.getDelay(actionbutton)
			print(f"Delay:{delay}\tAn error occurred when executing URL input or pressing execute button. Retrying")
			if delay != -1:
				self.countDown(delay)
			else:
				return delay
			self.driver.refresh()
			self.mainPageSelect(actionbutton)
			sleep(2)

	def loop(self, action, actionbutton, defaultwait=360, loops=10):
		if not self.AvailableActions[actionbutton]:
			print(f"{action} is not available right now")
			return -1
		count=0
		self.mainPageSelect(actionbutton)
		while count != loops:
			vidnum=count % len(self.vidURLS)
			# print(vidnum,count,len(self.vidURLS))
			print(f"Getting {action} for {self.vidURLS[vidnum]}")

			res=self.executionSteps(
				self.vidURLS[vidnum], action, actionbutton)
			if res == -1:
				count += 1
				continue

			sleep(5)

			try:
				# if "Successfully" in driver.find_element_by_xpath(XPathBases[actionbutton]+XPathList["successText"]).text:
				delay=self.getDelay(actionbutton)
				print(f"Delay is {delay}s\n")
				if delay == -1:
					self.driver.refresh()
					self.mainPageSelect(actionbutton)
					continue
				elif delay > 0:
					self.countDown(delay)
				else:
					self.countDown(defaultwait)

			except:
				print("action didnt work")
			count += 1

	def startOption(self):
		loops = 0
		while 1:
			print("What do you want to do?")
			if self.AvailableActions["viewsButton"]:
				print("1 - Get views")
			if self.AvailableActions["heartsButton"]:
				print("2 - Get hearts")
			if self.AvailableActions["commentsHeartsButton"]:
				print("3 - (FIRST) comments heart")
			if self.AvailableActions["followersButton"]:
				print("4 - Get followers")
			if self.AvailableActions["sharesButton"]:
				print("5 - Get Shares")
			if self.AvailableActions["livestreamButton"]:
				print("6 - Live Stream")
			opt=int(input("\n"))

			if loops <= 0:
				loops = int(input("How many times?"))
			
			if opt == 1 and self.AvailableActions["viewsButton"]:
				self.loop("Views", "viewsButton",loops=loops)
				break
			elif opt == 2 and self.AvailableActions["heartsButton"]:
				self.loop("Hearts", "heartsButton",loops=loops)
				break
			elif opt == 3 and self.AvailableActions["commentsHeartsButton"]:
				self.loop("Comment Hearts", "commentsHeartsButton",loops=loops)
				break
			elif opt == 4 and self.AvailableActions["followersButton"]:
				self.loop("Followers", "followersButton",loops=loops)
				break
			elif opt == 5 and self.AvailableActions["sharesButton"]:
				self.loop("Shares", "sharesButton",loops=loops)
				break
			elif opt == 6 and self.AvailableActions["livestreamButton"]:
				self.loop("Live Stream", "livestreamButton",loops=loops)
				break
			else:
				print(f"{opt} is NOT an Option")


def writelist(var, filename="options.json"):
	with open(filename, 'w', encoding="utf-8") as pl:
		json.dump(var, pl)


def loadlist(filename="options.json", default=[]):
	if not pathlib.Path(filename).exists():
		return default
	with open(filename, 'r', encoding="utf-8") as pl:
		pl=json.load(pl)
	return pl


def checkOPT(options):
	if "vidURLs" not in options or "serviceURL" not in options or "chromePath" not in options:
		print("\'chromePath\'/\'serviceURL\'/\'vidURLs\' is not defined in options.json")
		return False
	if len(options["vidURLs"]) == 0:
		print("There are no URLS in the list of videos \'vidURLs\'")
		return False
	if options["serviceURL"] == "":
		print("There is no URL in the \'serviceURL\'")
		return False
	if options["chromePath"] == "":
		print("\'chromePath\' cannot be an empty string")
		return False
	if not pathlib.Path(options["chromePath"]).exists():
		print(f"PATH: {options['chromePath']} doesn't exist")
		return False
	return True


def runloops(opts, b):
	for x in range(0, opts["loops"]):
		for action, val in opts["actions"].items():
			if val["loops"] > 0:
				b.loop(action, val["actionbutton"], loops=val["loops"])


if __name__ == "__main__":
	defaultOPT={
		"actions": {
			"Views": {
				"actionbutton": "viewsButton",
				"loops": 0
			},
			"Hearts": {
				"actionbutton": "heartsButton",
				"loops": 0
			},
			"Comment Hearts": {
				"actionbutton": "commentsHeartsButton",
				"loops": 0
			},
			"Followers": {
				"actionbutton": "followersButton",
				"loops": 0
			},
			"Shares": {
				"actionbutton": "sharesButton",
				"loops": 0
			},
			"Live Stream": {
				"actionbutton": "livestreamButton",
				"loops": 0
			}
		},
		"vidURLs": [
			"https://www.tiktok.com/@/video/",
			"https://www.tiktok.com/@/video/"
		],
		"serviceURL": "https://vipto.de/",
		"chromePath": "D:\\PATH\\chromedriver.exe",
		"loops": 0
	}
	if pathlib.Path("options.json").exists():
		print(f"loading opt")
		tempOPT=loadlist(default={})
		if checkOPT(tempOPT):
			defaultOPT=tempOPT
	else:
		print(f"writing opt")
		writelist(defaultOPT)
	if not checkOPT(defaultOPT):
		exit()

	b=tiktokBoost(
		vidURLS=defaultOPT["vidURLs"], serviceURL=defaultOPT["serviceURL"], chromePath=defaultOPT["chromePath"])
	# b.startOption()

	if defaultOPT["loops"] > 0:
		runloops(defaultOPT, b)
	else:
		b.startOption()
