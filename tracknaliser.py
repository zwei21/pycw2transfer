from tracks import *
import json
import urllib
import requests

def load_tracksfile(path):
	return json.load(path)

def query_tracks(start, end, n_tracks,  min_steps=1, max_steps=5,save=True):
	url = "http://ucl-rse-with-python.herokuapp.com/road-tracks/tracks/?start_point_x={}&start_point_y={}\
		&end_point_x={}&end_point_y={}&min_steps_straight={}&max_steps_straight={}&n_tracks={}".format(start[0], start[1],
		end[0], end[1],min_steps, max_steps, n_tracks )
	res_data = requests.get(url)
	data = json.loads(res_data.text)
	if save:
		with open("tracks_{}_{}_({}, {})_({}, {}).json".format(data["metadata"]["datetime"][:10], n_tracks, start[0], start[1], end[0], end[1]), 'w') as f:
			json.dump(data, f)
	return data

#query_tracks(start=(12, 15), end=(25, 46),min_steps=1, max_steps=40, n_tracks=30, save=True)
