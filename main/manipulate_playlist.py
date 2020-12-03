import pprint
import subprocess
import pickle
import os, shutil, sys
import logging
from collections import Counter

from sklearn import decomposition
import pandas as pd
import numpy as np

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util

pp = pprint.PrettyPrinter()


## primitive!
logger = logging.getLogger("manipulate_playlist")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("playlist.log")
logger.addHandler(file_handler)


class public_auth():

    """
    This is for accessing the API for on-user specific content

    Arguments:
        user            :ID of the user
    """

    def __init__(self, user):
        self.auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)


class playlist(public_auth):

    """
    Playlist object
    
    """

    def __init__(self, user: str, playlist_id: str):
        super().__init__(user)
        self.playlist = self.sp.playlist(playlist_id)
        self.playlist_tracks = self.playlist['tracks']['items']
        self.playlist_df = pd.DataFrame()
        # _, self.pca_components_ = self.pca()
        # self.playlist_uri = self.convert_uri(playlist_id)
        
    def convert_uri(self, playlist_id: str):
        """
        Converts id's of any format (URI, id, html) into uri 
        Arguments:
            playlist_id         :string storing the input

        Returns: 
            the URI of the playlist
        """
        if ":" not in playlist_id:
            return playlist_id
        if "/" in playlist_id:
            return playlist_id.split('/')[-1]
        return playlist_id.split(':')[-1]



    def get_artists(self):
        artist_list = []
        for song_obj in self.playlist_tracks:
            song_artists = []
            try:
                artists= song_obj['track']['artists']
                pp.pprint(artists)
                for artist in artists:
                    artist_uri = artist['uri']
                    song_artists.append(artist_uri)
            except KeyError:
                continue
            artist_list.append(song_artists)
        self.playlist_df['artists'] = artist_list


    def get_genres(self):
        if 'artists' not in self.playlist_df.columns:
            self.get_artists()
        genres_list = []
        def get_genre(artist_list):
            genre_counter = Counter()
            for artist in artist_list:
                artist_dict = self.sp.artist(artist)
                genre_counter.update(artist_dict['genres'])
            return genre_counter

        self.playlist_df['genres'] = self.playlist_df['artists'].apply(lambda x: get_genre(x))
        print(self.playlist_df)


    def get_audio_features(self):
        for song_obj in self.playlist_tracks:
            try:
                song_uri = song_obj['track']['uri']
            except KeyError:
                # A podcast or something
                continue
            song_features = self.sp.audio_features(song_uri)
            # this is bad practice! should be appending a list
            self.playlist_df = self.playlist_df.append(song_features[0], ignore_index = True)
        


    def pca(self, n_components = 4):
        # we ignore analysis_url, duration_ms, id, track_href, type, uri as logistical
        # we ignore key because songs can have any key; mode captures the major or minor characteristics
        pca_df = self.playlist_df[['acousticness', 'danceability','energy', 'instrumentalness', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']]
        pca = decomposition.PCA(n_components=n_components)
        pca.fit(pca_df)
        return pca_df, pca.components_


    def pickle_attribute(self, features: dict):
        """
        pickles features into /data/playlist_data/{self.playlist_uri}/

        Arguments:
            features          : dict[file_name, attribute]. Pickles attribute into "file_name.pkl"
        """
        outdir = f"../data/playlist_data/{self.playlist_uri}"

        try:
            os.makedirs(outdir)
        except OSError:
            logger.debug(f"{outdir} already exists")
    
        for feature_name in features:
            with open(f"{outdir}/{feature_name}.pkl", 'wb') as outfile:
                pickle.dump(features[feature_name], outfile)
        


if __name__ == "__main__":
    user_id = '22pzzk64jdu3j5atbs46avdhy'
    test_auth = public_auth(user_id)
    test_playlist = playlist(test_auth, 'spotify:playlist:1UFAdvEl2sA4p13ZmCteMf')
    test_playlist.get_genres()
    # test_playlist.get_audio_features()
    # print(test_playlist.playlist_df)
    # print(test_playlist.pca_components_)
    # test_playlist.pickle_attribute({"components": test_playlist.pca_components_, "playlist_df": test_playlist.playlist_df})


