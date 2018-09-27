import config
import tweepy
from tweepy import OAuthHandler
import csv
import time

# IMPORTANT : before running this script, please put your credentials in config.py file

# Class UserWithGeoInfos gives information about a Twitter user
class UserWithGeoInfos:
    def __init__(self):
        self.id = ""
        self.screen_name = ""
        self.utc_offset = ""
        self.location = ""
        self.user_profile_location_id = ""
        self.country = ""
        self.country_code = ""
        self.full_name = ""
        self.name = ""
        self.placeType = ""
        self.centroid_Latitude = ""
        self.centroid_Longitude = ""


# Process of the script
# Open the input Csv file "3 - ExampleForGettingUsersInformation/InputFileSomeUsersExample.csv"
# For each line, gets the screen name
# checks if within 15 minutes less than 850 calls were made , if yes continue process, if no sleep calculated time
# calls the Twitter get_user API to retrieve location_id information (for example : "Paris, France")
# calls to get_user api is limited to 900 within 15 minutes
# then calls with this location_id value the geo_id API to get the centroid of the location (code let without comments
# in the process but that can be commented because of the very low limitation of calls to this method in 15 minutes)
def process(entry):
    counter_screen_names = 0
    counter_screen_names_error = 0
    start_time = time.time()

    with open(entry, 'r') as csv_file:
        reader = csv.reader(csv_file)
        write_header()
        # Reading row by row
        for row in reader:
            try:
                # Following piece of code is due to the fact that Twitter limitates the call to its api
                # for the get_user method : it should be no more than 900 calls within 15 minutes (=900 seconds)
                if (((counter_screen_names + counter_screen_names_error) > 0)
                        and ((counter_screen_names + counter_screen_names_error) % 850 == 0)):
                    print("Elapsed time : " + str(int(time.time() - start_time)))
                    time.sleep(900 - (time.time() - start_time))
                    start_time = time.time()

                user_with_geo_infos = UserWithGeoInfos()

                screen_name = row[0]
                user = api.get_user(screen_name)
                user_with_geo_infos.id = user.id
                user_with_geo_infos.screen_name = screen_name
                user_with_geo_infos.utc_offset = user.utc_offset
                user_with_geo_infos.location = user.location

                # following piece of code could be removed because of 2 remarks:
                # 1 - Very Limited use of the api.geo_id within 15 minutes
                # 2 - Would have been interesting if was giving exact centroids for different places but for example:
                #     for location_id = "Paris, France", it will always give centroid : 48.85883375,2.320050211719896
                #     so not needed really, location_id is sufficient
                #if user.profile_location is not None:
                #    user_with_geo_infos.user_profile_location_id = user.profile_location["id"]
                #    geo_infos = api.geo_id(user_with_geo_infos.user_profile_location_id)
                #    user_with_geo_infos.country = geo_infos.country
                #     user_with_geo_infos.country_code = geo_infos.country_code
                #    user_with_geo_infos.full_name = geo_infos.full_name
                #    user_with_geo_infos.name = geo_infos.name
                #    user_with_geo_infos.placeType = geo_infos.place_type
                #    if geo_infos.centroid is not None:
                #        user_with_geo_infos.centroid_Latitude = geo_infos.centroid[1]
                #        user_with_geo_infos.centroid_Longitude = geo_infos.centroid[0]

                # Write in the output csv file location information corresponding to the user
                write_user_geo_infos_line(user_with_geo_infos)
                counter_screen_names = counter_screen_names + 1

            except BaseException as e:
                write_error_messages(row[0], str(e))
                counter_screen_names_error = counter_screen_names_error + 1
                print("Error on_data: " + str(e))

            # information written in the console about the evolving of the process
            print("OK : " + str(counter_screen_names) + " / Erreurs : " + str(counter_screen_names_error))


# Method writing the header of the output csv file
def write_header():
    with open("LaunchTestsAndSeeOutputsHere/3 - ExampleForGettingUsersInformation/UsersLocationInformation.csv", 'a', newline='') as csvFile:
        csv_writer = csv.writer(csvFile, delimiter=';')
        csv_writer.writerow(["UserId", "Screen_Name", "Utc_offset", "location", "ProfileLocationId", "Country", "Country_code", "Full_Name", "Name", "Place_Type", "Centroid_latitude", "Centroid_longitude"])


# Method writing a user line in the output csv file
def write_user_geo_infos_line(user_with_geo_infos):
    with open("LaunchTestsAndSeeOutputsHere/3 - ExampleForGettingUsersInformation/UsersLocationInformation.csv", 'a', newline='') as csvFile:
        csv_writer = csv.writer(csvFile, delimiter=';')
        csv_writer.writerow([user_with_geo_infos.id, user_with_geo_infos.screen_name, user_with_geo_infos.utc_offset, user_with_geo_infos.location, user_with_geo_infos.user_profile_location_id, user_with_geo_infos.country, user_with_geo_infos.country_code, user_with_geo_infos.full_name, user_with_geo_infos.name, user_with_geo_infos.placeType, user_with_geo_infos.centroid_Latitude, user_with_geo_infos.centroid_Longitude])


# Method writing a user line in the output error csv file
def write_error_messages(screen_name_error, exception_string):

    with open("LaunchTestsAndSeeOutputsHere/3 - ExampleForGettingUsersInformation/UsersWhichGotErrorsWhileProcessing.csv", 'a', newline='') as csvFile:
        csv_writer = csv.writer(csvFile, delimiter=';')
        csv_writer.writerow([screen_name_error, exception_string])


# Process
auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)
api = tweepy.API(auth)
process("LaunchTestsAndSeeOutputsHere/3 - ExampleForGettingUsersInformation/InputFileSomeUsersExample.csv")


