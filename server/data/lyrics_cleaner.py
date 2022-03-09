import re 

#We load the file with the names of the artists (created in the scraper script made with the Spotify API). And we create a list from it.
file = open("artist_names.txt", "r")

artist_names = []
for line in file:
  stripped_line = line.strip()
  artist_names.append(stripped_line)

file.close()

# We load the txt file with the lyrics
with open('letrasFinal.txt') as f:
    tex = f.read()

#For every artist, we delete all the ways it can be written (non-case sensitive)
for artist in artist_names:
    insensitive_artist = re.compile(re.escape(artist), re.IGNORECASE)
    tex = insensitive_artist.sub('', tex)

#Lets now remove the () , [] , x2, x3, x4, x5, x6, x7, x8, _
symbols = ['(', ')', '[', ']', '{', '}', ':' 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', '_', '....', '*', 'bis', 'coro','chorous']

for symbol in symbols:
    symbol_pat = re.compile(re.escape(symbol), re.IGNORECASE)
    tex = symbol_pat.sub('', tex)

#We create a new file with the cleaned lyrics.
f = open("letrasFinal_clean.txt","w+")
f.write(tex)
f.close()