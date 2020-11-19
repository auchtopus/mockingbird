import pprint
import subprocess

from sklearn import decomposition

import pandas as pd
import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util

pp = pprint.PrettyPrinter()

class public_auth():

    """
    This is for accessing the API for on-user specific content
    """

    def __init__(self, user):
        self.auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)


class playlist():

    """
    Store a playlist's name
    
    """

    def __init__(self, auth_obj: public_auth, playlist_id):
        self.sp = auth_obj.sp
        self.playlist = self.sp.playlist(playlist_id)
        self.playlist_tracks = self.playlist['tracks']['items']
        self.feature_df = self.get_audio_features()
        _, self.pca_components_ = self.pca()
        

    def get_audio_features(self):
        feature_df = pd.DataFrame()
        for song_obj in self.playlist_tracks:
            song_uri = song_obj['track']['uri']
            song_features = self.sp.audio_features(song_uri)
            feature_df =feature_df.append(song_features[0], ignore_index = True)
        return feature_df
        
    def pca(self, n_components = 4):
        # we ignore analysis_url, duration_ms, id, track_href, type, uri as logistical
        # we ignore key because songs can have any key; mode captures the major or minor characteristics
        pca_df = self.feature_df[['acousticness', 'danceability','energy', 'instrumentalness', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']]
        pca = decomposition.PCA(n_components=n_components)
        pca.fit(pca_df)
        return pca_df, pca.components_


if __name__ == "__main__":
    user_id = '22pzzk64jdu3j5atbs46avdhy'
    test_auth = public_auth(user_id)
    test_playlist = playlist(test_auth, 'spotify:playlist:1UFAdvEl2sA4p13ZmCteMf')
    test_playlist.get_audio_features()
    print(test_playlist.feature_df)
    print(test_playlist.pca_components_)


    


