from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from collections import Counter
import nltk

words = ['hello', 'hell', 'owl', 'hello', 'world', 'war', 'hello', 'war']

counter_obj = Counter(words)
counter_obj.most_common() 

class FriendsScript:
    def __init__(self, driver):
        self.driver = driver

    def scrape_NumEpisodes(self):
        self.driver.get("https://fangj.github.io/friends")

        # Dictionary Format: {Season 1: number of episodes, ..., season 10: number of episodes}
        self.Season_episodes = {}
        for i in range(10):
            try:
                season = self.driver.find_element_by_xpath(f"/html/body/ul[{i + 1}]")
            except:
                break
            self.Season_episodes[i + 1] = len(season.text.split('\n'))
        print(self.Season_episodes)
        

    def scrape_Scripts(self):

        # Set starting point (Season 1, Episode 1)
        season = 1
        episode = 1
        script_tags = []

        # Scrape data
        while True:
            base_url = f"https://fangj.github.io/friends/season/{str(season).zfill(2) + str(episode).zfill(2)}.html"
            self.driver.get(base_url)

            # Maximize window for the first iteration
            if season == '01' and episode == '01':
                self.driver.maximize_window()
            page_source = self.driver.page_source
            
            # pass in the page_source to BeautifulSoup
            soup = BeautifulSoup(page_source, 'lxml')
            
            # Get the entire script 
            script_full = soup.find_all('p')

            # Combine Scripts 
            
            for script in script_full:
                tokens = nltk.word_tokenize(script.text)
                tagged = nltk.pos_tag(tokens)
                for tag in tagged:
                    # Append alphanumeric tags (excludes )
                    if tag[1].isalnum() == True and tag[0].isalnum() == True:
                        script_tags.append(tagged)
            
            
            
            # When it reaches the final episode, go to the next season
            if self.Season_episodes[season] == episode:
                self.driver.quit()
                break
            episode += 1
        
        return script_tags

        
    
driver = webdriver.Chrome('C:\\NotionUpdate\\progress\\friends_NLP\\chromedriver.exe')
Friends = FriendsScript(driver)
Friends.scrape_NumEpisodes()
Friends.scrape_Scripts()

