# these should be the only imports you need

import requests
from bs4 import BeautifulSoup
import re # using re lib to search for the reportor's name if byline does not exist

# write your code here
# usage should be python3 part3.py

###############################################################################
# README                                                                      #
# Author: Xizi Wang                                                           #
# UMID: 24226806                                                              #
###############################################################################

def main():
    # set url
    BASE_URL = "http://michigandaily.com"
    # get html document
    html_doc = requests.get(BASE_URL).text
    # parse the html using beautiful soup
    soup = BeautifulSoup(html_doc, "html.parser")

    # get read most list and print each article and reportor
    read_most_list = soup.find("div",{"class": "panel-pane pane-mostread"}).find_all("li")
    print("Michigan Daily -- MOST READ")
    for article in read_most_list:
        # find and print title 
        article_title = article.find("a").string
        print(article_title)

        # get article url
        article_url = BASE_URL+article.find("a").get("href")
        
        # access to and parse article page
        html_doc = requests.get(article_url).text
        soup = BeautifulSoup(html_doc, "html.parser")

        # find and print reportor (only one)
        # if byline exist, print text in that span
        # else use regex to find the name
        article_reportor_ele = soup.find("div",{"class":"byline"})
        if(article_reportor_ele is not None):
            article_reportor = article_reportor_ele.find("a").string
            print("  By",article_reportor)
        else:
            pattern = "[ ]*[Bb][Yy][ ]*([A-aZ-z]* [A-aZ-z]*)"
            article_reportor = soup.find(text=re.compile(pattern))
            if article_reportor is not None:
                print(" ",article_reportor.string)
            else:
                print(" ",None)

if __name__ == "__main__":
    main()
