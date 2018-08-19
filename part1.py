# these should be the only imports you need
import tweepy
import nltk
import json
import sys
import re

###############################################################################
# README																	  #
# Author: Xizi Wang															  #
# UMID: 24226806															  #
###############################################################################

# write your code here
# usage should be python3 part1.py <username> <num_tweets>



# ARGUMENTS: the program takes two arguments--a twitter username and the number of tweets to analyze.

# OUTPUT: the program outputs the following:
# * the user name
# * the number of tweets analyzed
# * the five most frequent verbs that appear in the analyzed tweets
# * the five most frequent nouns that appear in the analyzed tweets
# * the five most frequent adjectives that appear in the analyzed tweets
# * the number of _original_ tweets (i.e., not retweets)
# * the number of times that the _original_ tweets in the analyzed set were favorited
# * the number of times that the _original_ tweets in the analyzed set were retweeted by others

# **To determine the five most frequent**, ties should be broken alphabetically, capitals before lowercase. (Check out Python stable sorting for a relatively easy way to handle this.)


# NOTES:
# * use `tweepy` for accessing the Twitter API
# * Use NLTK for analyzing parts of speech. Use NLTK's default POS tagger and tagset (this will use the [UPenn treebank tagset](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html))--you do NOT need to install any taggers or tagsets into NLTK.
# * "stop words": ignore any words that do not start with an alphabetic character `[a-zA-Z`], and also ignore 'http', 'https', and 'RT' (these show up a lot in Twitter)
# * a "verb" is anything that is tagged VB*
# * a "noun" is anything that is tagged NN*
# * an "adjective" is anything that is tagged JJ*



# SAMPLE OUTPUT:

# ```bash
# mwnewman$ python3 get_tweets.py umsi 12
# USER: umsi
# TWEETS ANALYZED: 12
# VERBS: are(4) being(3) is(3) improve(2) Join(2)
# NOUNS: umsi(8) UMSI(8) students(5) Join(5) amp(5)
# ADJECTIVES more(5) umsi(4) doctoral(2) new(2) social(2)
# ORIGINAL TWEETS: 8
# TIMES FAVORITED (ORIGINAL TWEETS ONLY): 26
# TIMES RETWEETED (ORIGINAL TWEETS ONLY): 18
# ```

# SAMPLE CSV FILE OUTPUT **inside a .csv file**
# ```txt
# Noun,Number
# umsi,8
# UMSI,8
# students,5
# Join,5
# amp,5
# ```

def list_to_str(the_list):
    res = []
    for x in the_list:
        res.append(x[0]+"("+str(x[1])+")")
    return " ".join(res)


def write_csv_file(the_list, filename): 
    with open("noun_data.csv", "w+") as file:
        file.write("Noun,Number")
    with open("noun_data.csv", "a") as file:
        for x in the_list:
            file.write("\n"+x[0]+","+str(x[1]))


def get_the_most_five(sentence_list, word_type):
    word_dict = dict()
    the_five_most_frequent = list()

    pattern = ""
    if(word_type == "VERB"):
        pattern = "VB*"
    elif(word_type == "NOUN"):
        pattern = "NN*"
    else:
        pattern = "JJ*"

    # get all words with specific tags
    for sentence in sentence_list:
        # get filtered sentence that does not contain stop words
        word_list = sentence.split(" ")
        filtered_sentence = ""
        for word in word_list:
            # skip spaces
            if len(word) == 0: continue
            # skip RT word
            if word == "RT": continue
            # skip url
            http_pattern = "http.*"
            if re.match(http_pattern, word): continue
            # skip words font start with an alphabetic character `[a-zA-Z`]
            if word[0].isalpha():
                filtered_sentence += " " + word
        # analyze the filtered sentence
        tokens = nltk.word_tokenize(filtered_sentence)
        tagged_tokens = nltk.pos_tag(tokens)
        for token in tagged_tokens:
            if re.match(pattern, token[1]):
                if not str(token[0][0]).isalpha() : continue
                # if word exists add 1, otherwize add the word
                word_dict[token[0]] = word_dict.get(token[0],0)+1

    # find 5 most ** words
    filtered_word_list = list()
    for word, count in word_dict.items():
        filtered_word_list.append([word,count])
    filtered_word_list.sort(key=lambda x: (-x[1],x[0]))
    return filtered_word_list[0:5]


def main(username, num_of_tweets):
    # declear and initialize varibales
    the_five_most_frequent_verbs = []
    the_five_most_frequent_nouns = []
    the_five_most_frequent_adjectives = []

    num_of_original_tweets = 0
    num_of_favor_original_tweets = 0
    num_of_retweeted_original_tweets = 0

    # Consumer keys and access tokens, used for OAuth
    consumer_key = 'QF03KwIjKtRTWDeqGWjpchgBb'
    consumer_secret = 'lvY39K8Fc9omwZq8HPVMwIApK4WuQgicZGjIoIhNyvJIBgNf3O'
    access_token = '785073452-uayvDGkjKjhoA5GO7mXvvzjLD7mx2sfdjuIRL1Mu'
    access_token_secret = 'WAuA1dan2ndAhOc1zDPRjULXwVUizCY4K6i4lt1Gyg2z7'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # get a list of status
    statuses = api.user_timeline(id=username, count=num_of_tweets)

    # get list of texts
    sentence_list = []
    for status in statuses:
        sentence_list.append(status._json.get("text"))

    # get a list of original tweets
    original_tweets = []
    for status in statuses:
        print(status._json)
        isRetweeted = status._json.get("retweeted")
        if(not isRetweeted):
            original_tweets.append(status._json)

    num_of_original_tweets = len(original_tweets)

    # retrive data
    for tweet in original_tweets:
        num_of_favor_original_tweets += tweet.get("favorite_count")
        num_of_retweeted_original_tweets += tweet.get("retweet_count")

    # get sorted the five most frequent ** list
    the_five_most_frequent_verbs = get_the_most_five(sentence_list,"VERB")
    the_five_most_frequent_nouns = get_the_most_five(sentence_list,"NOUN")
    the_five_most_frequent_adjectives = get_the_most_five(sentence_list,"ADJECTIVE")

    # save the 5 most frequent nouns to noun_data.csv
    write_csv_file(the_five_most_frequent_nouns, "noun_data.csv");

    # print output
    print("USER: "+username)
    print("TWEETS ANALYZED: "+str(num_of_tweets))
    print("VERBS: "+list_to_str(the_five_most_frequent_verbs))
    print("NOUNS: "+list_to_str(the_five_most_frequent_nouns))
    print("ADJECTIVES: "+list_to_str(the_five_most_frequent_adjectives))
    print("ORIGINAL TWEETS: "+str(num_of_original_tweets))
    print("TIMES FAVORITED (ORIGINAL TWEETS ONLY): "+str(num_of_favor_original_tweets))
    print("TIMES RETWEETED (ORIGINAL TWEETS ONLY): "+str(num_of_retweeted_original_tweets))


if __name__ == "__main__":
    if len(sys.argv)<3: 
        print("ERROR: invalid input")
    else: main(sys.argv[1],sys.argv[2]) 
