#!/data/data/com.termux/files/usr/bin/env python
import sys
import spotipy
import spotipy.util as util
import time

scope = 'user-library-modify,user-read-currently-playing,playlist-modify-private,playlist-modify-public,user-modify-playback-state'
username = os.environ.get('Spotify_Username')
clientID = os.environ.get('Spotify_Client_ID')
clientSecret = os.environ.get('Spotify_Client_Secret')
redirectURI = os.environ.get('Spotify_Redirect_URI')

token = util.prompt_for_user_token(username,scope,client_id=clientID,client_secret=clientSecret,redirect_uri=redirectURI)

if token:

	sp = spotipy.Spotify(auth=token)
	currTrack = sp.currently_playing()

	currTrackID = [currTrack['item']['uri']]
	remPlaylistID = currTrack['context']['uri']

	sp.next_track()
	sp.user_playlist_remove_all_occurrences_of_tracks(username,remPlaylistID,currTrackID)

