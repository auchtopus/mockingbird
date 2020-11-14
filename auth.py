import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy import util
import pprint
import subprocess



pp = pprint.PrettyPrinter()

class client:
    def __init__(self, user, init_file='./init.sh'):
        scope = 'playlist-read-private,' \
            ' playlist-read-collaborative,' \
            ' user-read-playback-state,' \
            ' user-modify-playback-state,' \
            ' user-read-currently-playing'
        subprocess.call(init_file) # initialize private tokens from init.sh
        self.user = user
        self.oauth = SpotifyOAuth(scope=scope)
        self.sp = spotipy.Spotify(auth_manager=self.oauth)

    def client_info(self):
        pp.pprint(self.sp.user(self.user))
        pp.pprint(self.sp.me())
        pp.pprint(self.sp.currently_playing())
        pp.pprint(self.sp.current_playback())

    def get_playlists(self):
        playlists = self.sp.user_playlists(self.user)
        playlist_items = []
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                full_playlist = self.sp.playlist_items(playlist['uri'])
                try:
                    playlist_items.append([(element['track']['name'], element['track']['id'], element['track']['artists'][0]['name'], element['track']['artists'][0]['id']) for element in full_playlist['items']])
                except KeyError:
                    continue
            # not sure what this does    
            if playlists['next']:
                playlists = self.sp.next(playlists)
            else:
                playlists = None
        return playlist_items




if  __name__ == "__main__":
    user_ID = '22pzzk64jdu3j5atbs46avdhy'
    test_client = client(user_ID)
    playlists = test_client.get_playlists()
    pp.pprint(playlists[0])
    test_client.client_info()
    

    
