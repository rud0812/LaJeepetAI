# Libs
import config
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pickle
import requests
from bs4 import BeautifulSoup as bs
import re

import time
from tqdm import tqdm
import string
from nltk.corpus import stopwords

from concurrent.futures import ThreadPoolExecutor

# 1.- SCRAPE ARTIST NAMES
##########################

# 1.1 -Define function to scrape info
def call_playlist(client,creator, playlist_id):
    # Create dict where to store the scraped data
    playlist_features_list = ["artist","album","track_name",  "track_id"]
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    
    playlist = client.user_playlist_tracks(creator, playlist_id)["items"]
    for track in playlist:
        # Create empty dict
        playlist_features = {}
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        
        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        
    return playlist_df


# 2.- GET LYRICS LINKS
#######################

# Scrape a list with most popular song names of artist and generate final url 

def song_scraper(url):
    response = requests.get(url,
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'})
    
    soup = bs(response.text,features="html.parser")
    elems = soup.find_all(class_="cnt-list-row -song")

    songs = [e['data-shareurl'] for e in elems]
    return songs


# 3.- SCRAPE LYRICS
####################

def lyrics_scraper(url_list):
    ly_list = []
    for i in tqdm(range(len(url_list))):
        time.sleep(1)
        response = requests.get(url_list[i],
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'})
        
        soup = bs(response.text, features="html.parser")
        elems = soup.find_all(class_="cnt-letra p402_premium")
        
        song = [e.text for e in elems]
        ly_list.append(song[0])
    return ly_list


# REQUEST PARALELLIZATION
##########################

def lyric_scraper(web_content):

    soup = bs(web_content, features="html.parser")
    elems = soup.find_all(class_="cnt-letra p402_premium")

    song = [e.text for e in elems]
    return song[0]
 
def download_lyric(url):
    try:
        response = requests.get(url, stream=True)
        lyric = lyric_scraper(response.text)
        open('lyrics.txt', 'a').write(lyric + '\n')
        return lyric
    except requests.exceptions.RequestException as e:
       print(e)
 
def runner(url_list):
    threads = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        for url in url_list:
            # executor.map(download_lyric,url_list)
            threads.append(executor.submit(download_lyric,url))


# 4.- PRE-PROCESSING 
#####################

# Text pre-processing function
def clean_lyrics(song):

    """
    Very basic text pre-processing function consisting on the following steps:
    - Remove punctuation signs
    - Split songs' sentences
    - Lowercase words
    - Split/Tokenize song
    """

    words = song.replace("'","").replace("(","").replace(")","").replace(".","")
    words = re.sub(r'(?<![A-Z\W])(?=[A-Z])', "\n", words)
    words = words.lower()
    final_words = words.split('\n')
    final_words = ('\n').join(final_words)

    return final_words