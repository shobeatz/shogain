import spotipy
import sys
import os
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import pandas as pd
import itertools
import json
import gcsfs
# import s3fs
from datetime import datetime
# import boto3
from pandas.core.computation import scope
from spotipy import SpotifyOAuth


def spotiflow_main():
    
    ## for use with SpotifyClientCredentials
    client_id = "ea47669c3d944a7f8ec4fc4232a4ac11"
    client_secret = "b13f5d79c372416e9726d3246b93a8a1"

    refresh_token = "AQBTALVFezh0s4DgKKUz3muo24eA4pSfgIhiUG0-r1KwL9MEs7U2_erb9RmuZcwxAjSnvc_JFdwuM1WvxBU6fzWefyhS9j7kTW8WQ1h64Nl6q_CRm8slyZNYUV29d4-gb18"                              

    ## for use with SpotifyClientCredentials & SpotifyOAuth
    redirect_uri = "http://localhost:5000/redirect/"
    scope = "user-library-modify"


    # import requests

    # # Replace 'your_client_id', 'your_client_secret', and 'your_refresh_token' with your actual Spotify Developer credentials and refresh token
    # client_id = "ea47669c3d944a7f8ec4fc4232a4ac11"
    # client_secret = "b13f5d79c372416e9726d3246b93a8a1"
    # refresh_token = "AQBTALVFezh0s4DgKKUz3muo24eA4pSfgIhiUG0-r1KwL9MEs7U2_erb9RmuZcwxAjSnvc_JFdwuM1WvxBU6fzWefyhS9j7kTW8WQ1h64Nl6q_CRm8slyZNYUV29d4-gb18"                              

    # # Spotify Accounts service endpoint
    # token_url = "https://accounts.spotify.com/api/token"

    # # Request body parameters
    # data = {
    #     'grant_type': 'refresh_token',
    #     'refresh_token': refresh_token,
    #     'client_id': client_id,
    #     'client_secret': client_secret,
    # }

    # # Make the POST request to refresh the access token
    # response = requests.post(token_url, data=data)

    # # Parse the response JSON
    # response_data = response.json()

    # # Extract the new access token
    # new_access_token = response_data.get('access_token')

    # # Now you can use the new access token for Spotify API requests


    # ## defining our working tracks & users

    # track_uri = "spotify:track:443hE8XxCysK9EjHjsRO9x"                       # URI for Campfire
    # artist_uri = "spotify:artist:7hMeb0h2KYV3AqAlNAApfM"                     # URI for Shobeatz
    # user_uri = "spotify:user:313b4azrbbixbfns24wadcbxlhie"                   # URI for Shobhit Chauhan
    # user_id = "313b4azrbbixbfns24wadcbxlhie"                                 # ID for Shobhit Chauhan


    # # creating Spotify object via SpotifyClientCredentials

    # spotipy_object = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials(
    #                                  client_id, 
    #                                  clien_secret))


    ## authorization via SpotifyOAuth; refreshing accesss token; creating spotipy_object

    auth_manager=SpotifyOAuth(client_id, 
                            client_secret, 
                            redirect_uri, 
                            scope)
    auth_manager.refresh_access_token(refresh_token)

    spotipy_object = spotipy.Spotify(auth_manager=auth_manager)


    # # track feature analysis using track_uri

    # track_feat = spotipy_object.audio_features(track_uri)
    # for items in track_feat:
    #     print(items)
    #     print(items.get('danceability'))                                   # loudness for Campfire


    # for key, value in liked_anal.items():
    #     print(key, value)


    ## api hit #1 for first batch of liked tracks

    limit = 50
    offset = 0

    liked_anal = spotipy_object.current_user_saved_tracks(limit=limit, offset=offset)              # limit returns the number of 'items' (max 50)

    ## creating a seperate all liked track data (not necessary)
    liked_anal_all = liked_anal.copy()

    ## will contain all info for all liked tracks
    all_liked_tracks_all = []

    for liked_track_name in liked_anal_all['items']:
        # liked_tracks_name = liked_track_name['track']
        all_liked_tracks_all.append(liked_track_name['track'])


    ## api hit #2 for all batches of liked tracks

    ## Checking if there are more tracks
    while liked_anal_all['next']:
        offset += limit
        liked_anal_all = spotipy_object.current_user_saved_tracks(limit=limit, offset=offset)               
            
    ## adding the next set of results into all_tracks 
        for liked_track_name in liked_anal_all['items']:
            # liked_tracks_new = liked_track['track']
            all_liked_tracks_all.append(liked_track_name['track'])

    print(all_liked_tracks_all)


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

    track_name = pd.DataFrame(name_uri_list)
    print(track_name)


    ## creating a list of all liked track uris

    all_liked_tracks_uri = track_name.uri.to_list()
    print(all_liked_tracks_uri)


    # # creating a seperate uri specific liked track data 
    # liked_anal_uri = liked_anal.copy()

    # # creating seperate current_user_saved_tracks parameters for uri data
    # limit1 = 50
    # offset1 = 0

    # # will contain uri for all liked tracks
    # all_liked_tracks_uri = []

    # for liked_track in liked_anal_uri['items']:
    #     # liked_tracks = liked_track_uri['track']['uri']
    #     all_liked_tracks_uri.append(liked_track['track']['uri'])

    # # Checking if there are more tracks
    # while liked_anal_uri['next']:
    #     offset1 += limit1
    #     liked_anal_uri = spotipy_object.current_user_saved_tracks(limit=limit1, offset=offset1)               
            
    # # adding the next set of results into all_tracks 
    #     for liked_track in liked_anal_uri['items']:
    #         # liked_tracks_new = liked_track['track']['uri']
    #         all_liked_tracks_uri.append(liked_track['track']['uri'])

    # all_liked_tracks_uri


    ## api hit 3 for all liked track features; creating tracklist by using the last created list & uri as an iterable

    all_track_anal = []

    for track in all_liked_tracks_uri:
        track_anal = spotipy_object.audio_features(track)
        all_track_anal.append(track_anal)

    print(all_track_anal)


    ## creating a df of all the liked tracks

    track_list = [] 

    for track_features in all_track_anal:
        ## getting individual lists of track dictionaries
        # print(track_features)

        for features in track_features:
            ## getting the actual track dictionaries from the individual lists
            # print(features)

            ## appending the track dictionaries into a single list & creating a df
            track_list.append(features)
            # print(track_list)
            track_df = pd.DataFrame(track_list)

    print(track_df)



    # # Another way to do the above step using list comprehension

    # flat_list = [item for sublist in all_track_anal for item in sublist]
    # df = pd.DataFrame(flat_list)


    main_df = track_df.merge(track_name, on = 'uri')
    # main_df


    main_df = main_df.sort_values(by='danceability',ascending=False).reset_index(drop=True)
    # main_df


    # main_df.info()


    dance_df = main_df.loc[main_df.danceability > 0.6]


    dance_df.to_csv("gs://af-landing-bucket/dance_df.csv", index = False)


