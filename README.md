# TikTok-Booster
Ability to boost VIEWS, HEARTS, COMMENT HEARTS, FOLLOWERS, SHARES, LIVE STREAM VIEWS

# Requirements
Selenium(Use pip) and https://chromedriver.chromium.org/downloads
You can't use a VPN

# Problems
- If the website in line 105 stops working the script becomes useless
- Any of the services offered by the website can stop working at any time in which case you have to stop the script and choose a different one

# Usage
1) Open options.json
2) Replace chromedriver path in line 33 with you own (add .exe at the end if on Windows)
	> "D:\\PATH\\chromedriver.exe"
3) Change the Loops value in lie 34 this will determine how many times the group of actions selected will be repeated
4) Change the loops values in line 5, 9, 13, 17, 21, and 25
	This will determine how many times you want each service to run before moving on to the next service
5) Paste TikTok video URL inside the quotes in line 29
	>"https://www.tiktok.com/@/video/",

	5a) You can use more then one video URL at a time just copy and paste line 29 after line 29 and replace the URL in the quotes, this will divide the service between all of the videos listed
	>"https://www.tiktok.com/@/video/",
	>"https://www.tiktok.com/@/video2/",
) Save and close

# Start
1) Start the bot with `python bt.py`
2) Insert the Captcha
3) Hit ENTER
4) The value of "loops" in line 34 is greater than 0 then all of the services selected on the json file will run otherwise you will be asked to choose one service and how many times you want 	to run it