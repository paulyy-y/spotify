import csv

import spotipy
# import pandas
import spotipy.util as util

from input_vars import *

token = util.prompt_for_user_token(username=user_logon,
                                   scope=scope,
                                   client_id=SPOTIPY_CLIENT_ID,
                                   client_secret=SPOTIPY_CLIENT_SECRET,
                                   redirect_uri=redirect_uri)

sp = spotipy.Spotify(auth=token)


def get_user_playlists(user):
    user_playlist = sp.user_playlists(user)
    plist_uri = []
    for x in user_playlist['items']:
        plist_uri.append(x['uri'])
    return plist_uri


def get_tracks(playlists):
    tracks = []
    for x in playlists:
        playlist_tracks = sp.playlist_tracks(playlist_id=x, fields='items')
        tracks.append(playlist_tracks)
    return tracks


def get_songs(tracks):
    songs = []
    for x in tracks:
        for y in x['items']:
            song = y['track']['name']
            added = y['added_at']
            # songs.append(["{},{}".format(song, added)])
            songs.append([song, added])
    return songs


def write_output(data, title):
    header = ['song', 'date']
    with open(title, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows([['song', 'added_time']])
        writer.writerows(songs)


playlists = get_user_playlists(user_target)
tracks = get_tracks(playlists)
songs = get_songs(tracks)

write_output(songs, 'songs.csv')
