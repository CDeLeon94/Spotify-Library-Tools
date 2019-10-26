#!/data/data/com.termux/files/usr/bin/env python
'''
    If playing your own playlist, will shuffle it in place utilizing python's random.shuffle() utility
'''

import spotipy
import spotipy.util as util
import random
from math import ceil

scope = 'user-library-modify,user-read-currently-playing,playlist-modify-private,playlist-modify-public,user-modify-playback-state'
username = os.environ.get('Spotify_Username')
clientID = os.environ.get('Spotify_Client_ID')
clientSecret = os.environ.get('Spotify_Client_Secret')
redirectURI = os.environ.get('Spotify_Redirect_URI')


def user_playlist_replace_unl_tracks(username, playlist, tracks):
    chunks = ceil(len(tracks)/100)
    for i in range(chunks):
        if i == 0:
            sp.user_playlist_replace_tracks(username, playlist, tracks[i*100:(i+1)*100])
        else:
            sp.user_playlist_add_tracks(username, playlist, tracks[i*100:(i+1)*100])


token = util.prompt_for_user_token(username,scope,client_id=clientID,client_secret=clientSecret,redirect_uri=redirectURI)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    currTrack = sp.currently_playing()
    currContext=currTrack['context']

    if currContext['type']=='playlist' and username in currContext['uri']:
        playlist = currContext['uri']

        results = sp.user_playlist(username, playlist,fields="name,tracks,next")

        tracks = results['tracks']

        all_songs = []


        for song in tracks['items']:
            all_songs.append(song['track']['uri'])

        while tracks['next']:
            tracks = sp.next(tracks)
            for song in tracks['items']:
                all_songs.append(song['track']['uri'])

        random.shuffle(all_songs)
        user_playlist_replace_unl_tracks(username, playlist, all_songs)
