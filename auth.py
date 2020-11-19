import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import util
import pprint
import subprocess



pp = pprint.PrettyPrinter()

class user_auth():

    """
    This component is for user-facing information requiring authentication.
    """

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
        self.playlists = self.sp.user_playlists(self.user)

    def verify_client_info(self):
        pp.pprint(self.sp.user(self.user))
        pp.pprint(self.sp.me())
        pp.pprint(self.sp.currently_playing())
        pp.pprint(self.sp.current_playback())

    


if  __name__ == "__main__":
    user_ID = '22pzzk64jdu3j5atbs46avdhy'
    test_client = user_auth(user_ID)
    test_client.verify_client_info()
    pp.pprint(test_client.playlists.keys())
    pp.pprint(test_client.sp.playlist('spotify:playlist:4BRkBYNyxarH79iktrTCAw'))
    pp.pprint(test_client.sp.playlist('spotify:playlist:4BRkBYNyxarH79iktrTCAw')['tracks']['items'][0])   
     

    

    