#!/data/data/com.termux/files/usr/bin/env python
import sys
import spotipy
import spotipy.util as util
import time
import os

scope = 'user-library-modify,user-read-currently-playing,playlist-modify-private,playlist-modify-public,user-modify-playback-state'
username = os.environ.get('Spotify_Username')
clientID = os.environ.get('Spotify_Client_ID')
clientSecret = os.environ.get('Spotify_Client_Secret')
redirectURI = os.environ.get('Spotify_Redirect_URI')

token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI)

if token:

	sp = spotipy.Spotify(auth=token)
	sp.trace_out = True
	currTrack = sp.currently_playing()

	print("\n\n\n")
	time.sleep(1)
	currTrack = sp.currently_playing()

	# read in parameters passed through the termux tasker action
	addPlaylistID = sys.argv[1]
	boolRemove = ( sys.argv[2] == "on" )
	currTrackID=[sp.currently_playing()['item']['uri']]
	# remove the song from the playlist (If its there... to prevent duplicates)
	# then add it to the playlist
	# todo: Check for duplicates and conditionally add the song
	sp.user_playlist_remove_all_occurrences_of_tracks(username,addPlaylistID,currTrackID)
	sp.user_playlist_add_tracks(username,addPlaylistID,currTrackID)

	# Add the song to the library aka save the track
	sp.current_user_saved_tracks_add(tracks=currTrackID)

	if boolRemove:
		currContextType = currTrack['context']['type']
		currContextURI = currTrack['context']['uri']
		if currContextType == 'playlist' and username in currContextURI and currContextURI != addPlaylistID :
			sp.user_playlist_remove_all_occurrences_of_tracks(username,currContextURI,currTrackID)
