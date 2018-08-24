# CapstoneAirPollution
Working well with PyCharm and python3.6

Requires also following packagings : tweepy, jsonpickle, selenium

Contains 3 python scripts

"1 - TwitterCrawlWithSelenium.py" :

    - Crawls Twitter advanced search results for specific keyword(s) at specific periods thanks to Selenium
    - When script executed, results are stored in csv files with information on posted messages in the 1 - ExampleForCrawlingTwitter folder
    - Selenium tests can be done with 3 possible navigators thanks to this piece of code:
      browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
      or
      browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
      or
      browser = webdriver.Opera(executable_path='/usr/local/bin/operadriver')

"2 - GetMostUsedWordsAndCountsFromMessages.py" : 

    - From a csv file having the format of the output got from 1 - TwitterCrawlWithSelenium.py
    - When script executed, displays in the console the words which appear the most in the tweet messages and their counts

3 - GetUsersLocationInformation.py :

    - Important: Requires config.py to be filled with Twitter credentials
    - From a csv file having one only column the screenName of users, will get location information about the users 
      whose screenNames are present in the input CSV file
    - When script exectuted, results are stored in an output CSV file in the 3 - ExampleForGettingUsersInformation folder

The config.py file should be updated using your own Twitter app credentials that you can obtain on www.app.twitter.com
