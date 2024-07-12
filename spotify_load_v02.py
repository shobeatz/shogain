import spotipy
import sys
import os
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import pandas as pd
import itertools
import json
# import s3fs
from datetime import datetime
# import boto3
from pandas.core.computation import scope
from spotipy import SpotifyOAuth


def spotiflow_main():

    ## defing SpotifyOAuth params; authorization via SpotifyOAuth; refreshing accesss token; creating spotipy_object
    client_id = "ea47669c3d944a7f8ec4fc4232a4ac11"
    client_secret = "b13f5d79c372416e9726d3246b93a8a1"
    redirect_uri = "http://localhost:5000/redirect/"
    scope = "user-library-modify"
    refresh_token = "AQBTALVFezh0s4DgKKUz3muo24eA4pSfgIhiUG0-r1KwL9MEs7U2_erb9RmuZcwxAjSnvc_JFdwuM1WvxBU6fzWefyhS9j7kTW8WQ1h64Nl6q_CRm8slyZNYUV29d4-gb18"                              

    auth_manager=SpotifyOAuth(client_id, 
                            client_secret, 
                            redirect_uri, 
                            scope)
    
    auth_manager.refresh_access_token(refresh_token)

    spotipy_object = spotipy.Spotify(auth_manager=auth_manager)


    ## API hit #1 for first batch of liked tracks
    limit = 50
    offset = 0
    liked_anal = spotipy_object.current_user_saved_tracks(limit=limit, offset=offset)              # limit returns the number of 'items' (max 50)

    ## creating a seperate all liked track data (not necessary)
    liked_anal_all = liked_anal.copy()

    ## will contain all info for all liked tracks (first batch of liked tracks)
    all_liked_tracks_all = []
    for liked_track_name in liked_anal_all['items']:
        # liked_tracks_name = liked_track_name['track']
        all_liked_tracks_all.append(liked_track_name['track'])


    ## API hit #2 for all remaining batches of liked tracks 
    while liked_anal_all['next']:
        offset += limit
        liked_anal_all = spotipy_object.current_user_saved_tracks(limit=limit, offset=offset)               
            
        ## adding the next set of results into all_liked_tracks_all 
        for liked_track_name in liked_anal_all['items']:
            # liked_tracks_new = liked_track['track']
            all_liked_tracks_all.append(liked_track_name['track'])


    ## getting the liked track names & uris
    name_uri_list = []

    for all_liked_tracks in all_liked_tracks_all:
        # print(all_liked_tracks)
        ## getting value of name & uri keys
        trackname = all_liked_tracks.get('name')
        trackuri = all_liked_tracks.get('uri')

        ## below method also works to extract values of a key
        # trackname = all_liked_tracks['name']
        # trackuri = all_liked_tracks['uri']
            
        ## creating a dictionary; appending dictionary to name_uri_list
        name_uri_dict = {'name': trackname, 'uri': trackuri}
        name_uri_list.append(name_uri_dict)


    ## creating a df from the trackname & trackuri list
    track_name = pd.DataFrame(name_uri_list)


    ## creating a list of all liked track uris using track_name df (could've been done using trackuri but anyway)
    all_liked_tracks_uri = track_name.uri.to_list()


    ## api hit 3 for all liked track features; creating tracklist by using the last created list & uri as an iterable
    all_track_anal = []
    for track in all_liked_tracks_uri:
        track_anal = spotipy_object.audio_features(track)
        all_track_anal.append(track_anal)

     
    ## creating a df of all the liked tracks; getting individual lists of track dictionaries
    track_list = []
    for track_features in all_track_anal:
        # print(track_features)

        ## getting the actual track dictionaries from the individual lists
        for features in track_features:
            # print(features)

            ## appending the track dictionaries into a single list & creating a df
            track_list.append(features)
            # print(track_list)
            track_df = pd.DataFrame(track_list)


    ## merging track_name into track_list df to create main_df; printing for check
    main_df = track_df.merge(track_name, on = 'uri')
    main_df = main_df.sort_values(by='danceability',ascending=False).reset_index(drop=True)
    print(main_df[0:5])


    ## loading the output into GCS as a trigger for Clustering
    main_df.to_csv("gs://af-landing-bucket/main_df.csv", index = False)

spotiflow_main()