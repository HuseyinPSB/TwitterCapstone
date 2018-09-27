import csv
import string
import os
import fnmatch
import re
from collections import Counter


# This method checks each word of a list of words and removes some special characters
def remove_punctuation(list_of_words):
    cleant_list_of_words = ""
    for word in list_of_words:
        # If char is not punctuation, add it to the result.
        # string.punctuation contains these symbols:
        #  !, ", #, $, %, &, ', (, ), *, +, , ,- , . , / , : , , ; , < , = , >
        #  ? , @ , [ , \ , ], ^ , _ , ` , { , | , } , ~
        if word not in string.punctuation:
            cleant_list_of_words += word

    return cleant_list_of_words


# Method which adds words in the total list of words
def read_words(words, msg_content_cleant):
    list_of_words_to_ignore = [' un ', ' une ', ' unes ', ' le ', ' la ', ' les ', ' de ', ' du ', ' des ', ' le ',
                               ' et ', ' le ', ' la ', ' ou ', ' le ', ' la ', ' or ', ' les ', ' que ', ' qui ',
                               ' que ', ' où ', ' quand ', ' car ', ' mais ', ' on ', ' je ', ' tu ', ' il ', ' elle ',
                               ' nous ', ' vous ', ' ils ', ' elles ', ' à ', ' au ', ' aux ', ' en ', ' dans ', ' in ',
                               ' pas ', ' sur ', ' sous ', ' pour ', ' contre ', ' par ', ' via ', " c'est ", " cest ",
                               " suis ", " es ", " est ", " sont ", " ce ", " ces ", " ça ", " cela ", " cette ",
                               " cettes ", " quel ", " quels ", " quelle ", " quelles ", " ai ", " as ", " a ",
                               " avons ", " avez ", " ont ", " ne ", " ni ", ' noise ', ' rock ', ' roll ', ' c ',
                               ' j ', ' l ', ' d ', ' m ', ' n ', ' s ', ' t ', ' y ', ' qu ', ' toujours ', ' jamais ',
                               ' plus ', ' moins ', ' avec ', ' sans ', ' chez ', ' eux ', ' oui ', ' non ', ' fait ',
                               ' se ', ' tout ', ' comme ', ' bien ', ' même ', ' sa ', ' son ', ' ses ', ' ma ',
                               ' mes ', ' mon ', ' ta ', ' ton ', ' tes ', ' si ', ' va ', ' aussi ', ' aujourd ',
                               ' hui ', ' « ', ' » ', ' notre ', ' votre ', ' nos ', ' vos ', ' être ', ' me ', ' te ',
                               ' se ', ' rien ', ' moi ', ' comment ', ' faut ', ' tous ', ' tout ', ' toutes ',
                               ' toute ', ' jusqu ', ' selon ', ' aller ', ' faire ', ' avant ', ' après ', ' après ',
                               ' coût ', ' coûte ', ' euros ', ' trop ', ' veut ', ' bon ', ' sera ', ' entre ',
                               ' depuis ', ' encore ', ' 20 ', ' idée ', ' très ', ' chaque ', ' an ', ' ans ',
                               ' leur ', ' peut ']

    # Here we remove all the words from the messages that would be in the list just above
    for word_to_ignore in list_of_words_to_ignore:
        msg_content_cleant = msg_content_cleant.replace(word_to_ignore, "  ")

    # we split the message cleant in many words separated by spaces and remove all words beginning by http
    tempo_words = msg_content_cleant.split()
    for word_position in range(len(tempo_words)-1, 0, -1):
        if tempo_words[word_position].startswith("http"):
            tempo_words.remove(tempo_words[word_position])

    words += tempo_words
    return words


# Method adding
def append_words_to_all_words_issued_from_all_messages(words, entry):
    with open(entry, 'r') as csv_file:
        reader = csv.reader(csv_file)

        # Reading row by row
        for row in reader:
            csv_line = ""
            for x in range(0, len(row)):
                csv_line += row[x]

            # The information we need is in the 3rd column,
            # but if we split just with ";" it can have weird behavior with some csvLines
            # so we split before the 4th column ";fr;" , then we split the result and get what is after the 2nd ";"
            # Then we remove all the http://.... and https://..... with a regex expression
            # then we replace some specific symbols from the message content
            # then we use the remove_punctuation method to remove other specific symbols
            msg_content_cleant = (csv_line.split(";fr;")[0].lower()).split(";")[2]
            msg_content_cleant = re.sub(r'/http\w+/', '', msg_content_cleant)
            msg_content_cleant = msg_content_cleant.replace("'", " ")
            msg_content_cleant = msg_content_cleant.replace("’", " ")
            msg_content_cleant = msg_content_cleant.replace('…', " ")
            msg_content_cleant = msg_content_cleant.replace('★', " ")
            msg_content_cleant = " " + remove_punctuation(msg_content_cleant) + " "
            read_words(words, msg_content_cleant)


# Main process
folder_name = "LaunchTestsAndSeeOutputsHere/2 - ExampleForGettingWordsCount"
pattern = "*.csv"

# Gets all csvFiles from the folder specified above
# declare all_words_issued_from_all_messages which will contain all the words contained in all the csv lines
# example : all_words_issued_from_all_messages = [ "pollution" , "paris" , "france" , "alerte" , "pollution",  ... ]
#           same word can be present many times in this variable, then we will do a count with the Counter method
listOfFiles = os.listdir(folder_name)
all_words_issued_from_all_messages = []
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, pattern):
            append_words_to_all_words_issued_from_all_messages(all_words_issued_from_all_messages, folder_name + "/" + entry)

# Counter counts the number off occurences of all words contained in the all_words_issued_from_all_messages
# We print the 200 words having the biggest count
count_each_word = Counter(all_words_issued_from_all_messages).most_common(200)

# This piece of code prints in the console mode the 75 words appearing most of times in the messages contents
for searchedWord in count_each_word:
    searchedWord = str(searchedWord).replace("('", "")
    searchedWord = str(searchedWord).replace("', ", ";")
    searchedWord = str(searchedWord).replace(")", "")
    print(searchedWord)




