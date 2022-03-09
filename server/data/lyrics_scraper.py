""""
Script to connect to Spotify API and extract artists' names from 
the most popular reggaeton playlists.

"""
import utils_lyrics_scraper as utils
import pandas as pd
import pickle

# 1.- SCRAPE ARTIST NAMES
##########################

# Apply 1.1 and scrape artist names
playlist_list = ["03sDEv7FN58Mb9CJOs1Tgn", # reggaeton 2021
                "37i9dQZF1DX8SfyqmSFDwe",  # reggaeton mix 
                "5LTV57azwaid7dXfz5fzJu"]  # reggaeton antiguo

lists_artists = [utils.call_playlist("spotify",code) for code in playlist_list]  # connect to API and get info
list_artists = [item for sublist in lists_artists for item in sublist]           # list of lists to single list

list_artists = list(set(list_artists))                                           # remove duplicates
artist_list = [p.lower().replace(' ','-') for p in list_artists]                 # clean names' format
url_list = [ 'https://www.letras.com/' + artist +"/" for artist in artist_list]  # generate links to lyrics

# 2.- GET LYRICS LINKS
#######################

# Scrape a list with most popular song names of artist and generate final url 

final_urls_list = [utils.song_scraper(u) for u in url_list]
final_urls_list = [item for sublist in final_urls_list for item in sublist]

# Save final url list 
# with open('lista_links.pickle', 'wb') as handle:
#     pickle.dump(final_urls_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

# 3.- SCRAPE LYRICS
####################

utils.runner(final_urls_list)

# 4.- PRE-PROCESSING 
#####################

df = pd.read_csv("lyrics.txt",sep="\n",header = None, names=['song'])
df['clean_song'] = [utils.clean_lyrics(s) for s in df['song']]

# with open("letrasFinal.txt", "w") as text_file:
#     for cancion in df['clean_song']:
#         text_file.write(cancion + '\n\n')

