from pprint import pprint
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("What year do you want to travel to? Type the date in this format YYY-MM-DD: ")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
top_songs = response.text

soup = BeautifulSoup(top_songs, "html.parser")
all_songs = soup.find_all(name="h3", class_="a-no-trucate")
songs_title = [songs.getText().replace("\n\n\t\n\t\n\t\t\n\t\t\t\t\t", "").replace("\t\t\n\t\n", "") for songs in all_songs]

CLIENT_ID = ""
CLIENT_SCRET_KEY = ""
REDIRECT_URI = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SCRET_KEY,
        show_dialog=True,
        cache_path="token.txt",

    )
)
year = date.split("-")[0]
user_id = sp.current_user()["id"]
print(user_id)
spotify_song_uris = []
for song in songs_title:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uris = result['tracks']['items'][0]['uri']
        spotify_song_uris.append(uris)
    except IndexError:
        print(f"{song} is not available. Skipped")
print(len(spotify_song_uris))

playlist = sp.user_playlist_create(user=user_id, name=f"{date}Billboard100", public=False, )
the_playlist = sp.playlist_add_items(playlist_id=playlist["id"], items=spotify_song_uris)
print(playlist)
print(the_playlist)
