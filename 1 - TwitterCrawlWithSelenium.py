from selenium import webdriver
import jsonpickle
import time
import csv

# This python file crawls twitter for some specific words for a specific period and returns
# a csv file for each day containing information about the tweets crawled thanks to selenium functionnalities
# At the end of this file, see the explained process with one example


# Class containing useful information for running process
class ProcessInfos:

    nbRecordsPerOutputFile = 500
    automaticScrollDown = True
    # File output can be json or csv
    outputType = "csv"

    def __init__(self):
        self.counterTotal = 0
        self.counterLocal = 0
        self.counterScrollDown = 0
        self.searchedWithThisKeyword = ""
        self.searchedWithThisPeriod = ""
        self.scrollDownCounter = 0
        self.listPeriods = []
        self.listKeywords = []

    # Method that scrolls down the web page
    def scroll_down(self, browser):
        self.counterScrollDown = 0
        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            self.counterScrollDown = self.counterScrollDown + 1
            print("Scroll number " + str(self.counterScrollDown))
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(3)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script('return document.body.scrollHeight')

            if new_height == last_height:
                self.scrollDownCounter = self.counterScrollDown
                break

            last_height = new_height

    # Function that add keywords to a list of keywords
    def add_preset_keywords_related_with(self, type_of_keyword):

        if type_of_keyword == "pollution":
            self.listKeywords.append("pollution OR pollutions")

        if type_of_keyword == "pollutionAutres":
            self.listKeywords.append("pollu")
            self.listKeywords.append("polluant")
            self.listKeywords.append("polluante")
            self.listKeywords.append("polluantes")
            self.listKeywords.append("polluants")
            self.listKeywords.append("pollue")
            self.listKeywords.append("polluee")
            self.listKeywords.append("polluees")
            self.listKeywords.append("polluent")
            self.listKeywords.append("polluer")
            self.listKeywords.append("pollues")
            self.listKeywords.append("pollueur")
            self.listKeywords.append("pollueurs")
            self.listKeywords.append("polluez")
            self.listKeywords.append("pollut")
            self.listKeywords.append("polluti")
            self.listKeywords.append("pollutio")
            self.listKeywords.append("pollutionGlobal")
            self.listKeywords.append("pollutionparis")
            self.listKeywords.append("parispollution")

        if type_of_keyword == "qualite_air":
            self.listKeywords.append("qualité de l’air")

        if type_of_keyword == "irrespirable":
            self.listKeyWords.append("irrespirable OR irrespirables")

        if type_of_keyword == "particules":
            self.listKeywords.append("particule en suspension")
            self.listKeywords.append("particules en suspension")
            self.listKeywords.append("particule fine")
            self.listKeywords.append("particules fines")
            self.listKeywords.append("microparticule")
            self.listKeywords.append("microparticules")

        if type_of_keyword == "visibilite":
            self.listKeywords.append("visibilité")

        if type_of_keyword == "pm25or10":
            self.listKeywords.append("pm2.5 OR pm25 OR pm10")

    # Method which assures that a number is written in 2 digits : write_2_digit_number(9) = 09
    @staticmethod
    def write_2_digit_number(number):
        if number > 9:
            return str(number)
        else:
            return "0" + str(number)

    def add_period_to_list_periods(self, year, month, day_initial, day_final):
        for iDay in range(day_initial, day_final):
            rewritten_text = "since%3A" + str(year) + "-" + self.write_2_digit_number(month) \
                           + "-" + self.write_2_digit_number(iDay) + " until%3A" + str(year) \
                           + "-" + self.write_2_digit_number(month) + "-" + self.write_2_digit_number(iDay + 1)
            self.listPeriods.append(rewritten_text)

    # Junction from the end of 1 month to the 1st day of the following month
    def add_junction_from_end_of_month_to_beginning_of_next_month(self, year, month, last_day_of_month):
            rewritten_text = "since%3A" + str(year) + "-" + self.write_2_digit_number(month) \
                           + "-" + self.write_2_digit_number(last_day_of_month) + " until%3A" + str(year + 1 if month == 12 else year) \
                           + "-" + self.write_2_digit_number(month+1 if month < 12 else 1) + "-01"
            self.listPeriods.append(rewritten_text)

    # Process for a complete month
    def add_whole_month(self, year, month, last_day_of_month):
            self.add_period_to_list_periods(year, month, 1, last_day_of_month)
            self.add_junction_from_end_of_month_to_beginning_of_next_month(year, month, last_day_of_month )

    # Process for a complete year
    def add_all_days_for_a_whole_year(self, year):
        self.add_whole_month(year, 1, 31)
        if year == 2016:
            self.add_whole_month(year, 2, 29)
        else:
            self.add_whole_month(year, 2, 28)
        self.add_whole_month(year, 3, 31)
        self.add_whole_month(year, 4, 30)
        self.add_whole_month(year, 5, 31)
        self.add_whole_month(year, 6, 30)
        self.add_whole_month(year, 7, 31)
        self.add_whole_month(year, 8, 31)
        self.add_whole_month(year, 9, 30)
        self.add_whole_month(year, 10, 31)
        self.add_whole_month(year, 11, 30)
        self.add_whole_month(year, 12, 31)


    # Crawl process + writing of the csv or json file
    def crawl_n_write(self):
        url = "https://twitter.com/search?f=tweets&l=fr&q=" + searchToDo + " " + self.searchedWithThisPeriod
        print(url)

        browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        # browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        # browser = webdriver.Opera(executable_path='/usr/local/bin/operadriver')
        browser.get(url.replace(' ', '%20'))
        self.counterLocal = 0

        if self.automaticScrollDown:
            self.scroll_down(browser)

        all_tweets = browser.find_elements_by_class_name("tweet")
        for currentTweet in all_tweets:
            try:
                self.counterLocal = self.counterLocal + 1
                self.counterTotal = self.counterTotal + 1

                # Get data from web interface
                displayed_span_date = currentTweet.find_elements_by_class_name("_timestamp")
                tweet_content_div = currentTweet.find_elements_by_class_name("js-tweet-text-container")
                tweet_text_p = tweet_content_div[0].find_elements_by_class_name("js-tweet-text")
                from_whom = currentTweet.find_elements_by_class_name("FullNameGroup")
                to_whom = currentTweet.find_elements_by_class_name("username")
                profile_tweet_action_reply = currentTweet.find_elements_by_class_name("ProfileTweet-action--reply")
                profile_tweet_action_retweet = currentTweet.find_elements_by_class_name("ProfileTweet-action--retweet")
                profile_tweet_action_favorite = currentTweet.find_elements_by_class_name("ProfileTweet-action--favorite")

                # Instantiate new object and fill it
                tweet_infos = TweetInfos()

                tweet_infos.aDate = displayed_span_date[0].text
                tweet_infos.aDateEpochUnix = displayed_span_date[0].get_attribute("data-time")

                tweet_infos.bTweetText = tweet_content_div[0].text
                tweet_infos.bTweetTextLang = tweet_text_p[0].get_attribute("lang")

                tweet_infos.cFromWhom = from_whom[0].text
                tweet_infos.cToWhom = to_whom[0].text

                tweet_infos.dataTweetId = currentTweet.get_attribute("data-tweet-id")
                tweet_infos.dataPermalinkPath = "https://twitter.com" + currentTweet.get_attribute("data-permalink-path")
                tweet_infos.dataUserId = currentTweet.get_attribute("data-user-id")
                tweet_infos.dataName = currentTweet.get_attribute("data-name")
                tweet_infos.dataScreenName = currentTweet.get_attribute("data-screen-name")

                tweet_infos.eProfileTweetActionReply = profile_tweet_action_reply[1].find_elements_by_class_name("ProfileTweet-actionCountForPresentation")[0].text
                tweet_infos.eProfileTweetActionRetweet = profile_tweet_action_retweet[1].find_elements_by_class_name("ProfileTweet-actionCountForPresentation")[0].text
                tweet_infos.eProfileTweetActionFavorite = profile_tweet_action_favorite[1].find_elements_by_class_name("ProfileTweet-actionCountForPresentation")[0].text

                tweet_infos.fSearchedWithThisKeyword = self.searchedWithThisKeyword

                print("Total count :" + str(self.counterTotal) + " (Local count : " + str(self.counterLocal) + " out of between " + str((self.scrollDownCounter - 1) * 20) + " and " + str((self.scrollDownCounter + 1) * 20) + ")")
                print(tweet_infos.aDate)
                print(tweet_infos.bTweetText)

                number_sub_file = 1 + (self.counterLocal - 1) / self.nbRecordsPerOutputFile
                filename = fileNameRoot + "-" + str(int(number_sub_file)) + "." + self.outputType

                self.write_in_file(tweet_infos, filename)

            except BaseException as e:
                print("Error on_data: " + str(e))

        browser.quit()

    def clean_parameter(self, string_to_clean):
            return string_to_clean.replace("\n", "").replace("\r", "").replace("\t", "")

    def write_in_file(self, tweet_infos, filename):

        if self.outputType == "json":
            with open("LaunchTestsAndSeeOutputsHere/1 - ExampleForCrawlingTwitter/" + filename, 'a') as f:
               f.write(jsonpickle.encode(tweet_infos, unpicklable=False) + '\n')

        if self.outputType == "csv":
            with open("LaunchTestsAndSeeOutputsHere/1 - ExampleForCrawlingTwitter/" + filename, 'a', newline='') as csvFile:
                csv_writer = csv.writer(csvFile, delimiter=';')
                if self.counterLocal % self.nbRecordsPerOutputFile == 1:
                    csv_writer.writerow(["aDate", "aDateEpochUnix", "bTweetText", "bTweetTextLang", "cFromWhom", "cToWhom", "dataTweetId", "dataPermalinkPath", "dataUserId", "dataName", "dataScreenName", "eProfileTweetActionReply", "eProfileTweetActionRetweet", "eProfileTweetActionFavorite", "fSearchedWithThisKeyword"])

                csv_writer.writerow([self.clean_parameter(tweet_infos.aDate), self.clean_parameter(tweet_infos.aDateEpochUnix), self.clean_parameter(tweet_infos.bTweetText), self.clean_parameter(tweet_infos.bTweetTextLang), self.clean_parameter(tweet_infos.cFromWhom), self.clean_parameter(tweet_infos.cToWhom), self.clean_parameter(tweet_infos.dataTweetId), self.clean_parameter(tweet_infos.dataPermalinkPath), self.clean_parameter(tweet_infos.dataUserId), self.clean_parameter(tweet_infos.dataName), self.clean_parameter(tweet_infos.dataScreenName), self.clean_parameter(tweet_infos.eProfileTweetActionReply), self.clean_parameter(tweet_infos.eProfileTweetActionRetweet), self.clean_parameter(tweet_infos.eProfileTweetActionFavorite), self.clean_parameter(tweet_infos.fSearchedWithThisKeyword)])


# Class containing useful information about the tweet coming from the crawled web pages
class TweetInfos:
    def __init__(self):
        # Displayed date
        self.aDate = ""
        # Epoch Unik date (number of seconds from 1 January 1970)
        self.aDateEpochUnix = ""
        # Text content of the tweet
        self.bTweetText = ""
        # language of the div containing the text
        self.bTweetTextLang = ""
        # Who wrote the tweet
        self.cFromWhom = ""
        # To whom the tweet is destinated
        self.cToWhom = ""
        # Url to the tweet
        self.dataPermalinkPath = ""
        # Tweet id
        self.dataTweetId = ""
        # User id
        self.dataUserId = ""
        # User dataname
        self.dataName = ""
        # User datascreen name
        self.dataScreenName = ""
        # Number of replies to this tweet
        self.eProfileTweetActionReply = ""
        # Number of times the tweet was retweeted
        self.eProfileTweetActionRetweet = ""
        # Number of times the tweet was put in favourite
        self.eProfileTweetActionFavorite = ""
        # Search keyword
        self.fSearchedWithThisKeyword = ""


process_infos = ProcessInfos()

# 1) CHOOSE KEYWORDS TO CRAWL
# 2 possibilities :
# use the "add_preset_keywords_related_with" method (preset keywords are : "pollution", "pollutionAutres",
#                                                        "qualite_air", "irrespirable", "particules",  "pm25or10"
# or specify one specific keyword directly
process_infos.add_preset_keywords_related_with("pollution")
# processInfos.listKeywords.append("specific_keyword")

# 2) SPECIFY PERIOD(S) OF TIME TO BE CRAWLED
# add_period_to_list_periods(2015, 9, 12, 14) means a period from 12 September to 14 September 2015
# it will do successively the following searches:
# https://twitter.com/search?f=tweets&l=fr&q=pollution OR pollutions since%3A2015-09-12 until%3A2015-09-13
# https://twitter.com/search?f=tweets&l=fr&q=pollution OR pollutions since%3A2015-09-13 until%3A2015-09-14
# and creates 2 csv files, 1 for each day
process_infos.add_period_to_list_periods(2015, 9, 12, 14)

# for having a whole month (example here for May 2013)
#process_infos.add_whole_month(2013, 5, 31)
# for having a whole year (example here for year 2014)
#process_infos.add_all_days_for_a_whole_year(2014)

# 3) CRAWL AND WRITE CSV FILE OR JSON FEED
for keyword in process_infos.listKeywords:
    print(keyword)
    searchToDo = keyword
    process_infos.searchedWithThisKeyword = keyword
    time.sleep(4)
    for period in process_infos.listPeriods:
        fileNameRoot = keyword + " " + str(period).replace("%3A", " ")
        process_infos.searchedWithThisPeriod = period
        process_infos.crawl_n_write()


