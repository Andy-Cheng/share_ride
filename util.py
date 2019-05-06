# Author: Andy Cheng
# Email: andytony56791@gmail.com

import googlemaps
import numpy as np
import pandas as pd
import random

# Google Map API
api_key = 'Your api key'
gmaps = googlemaps.Client(key = api_key)
'''
basic response of distance_matrix:
{'destination_addresses': ['10491台灣台北市中山區敬業三路20號', '110台灣台北市信義區信義路五段7號台北101大樓'], 'origin_addresses': ['10617台灣台北市大安區羅斯福路四段1號'], 'rows': [{'elements': [{'distance': {'text': '10.6 公里', 'value': 10613}, 'duration': {'text': '20 分', 'value': 1177}, 'status': 'OK'}, {'distance': {'text': '3.8 公里', 'value': 3816}, 'duration': {'text': '13 分', 'value': 808}, 'status': 'OK'}]}], 'status': 'OK'} 
'''

def write_to_excel(results):
    with pd.ExcelWriter('路線.xlsx') as writer:  # doctest: +SKIP
        route_index = 1
        for result in results:
            (way_points, num_passengers, durations) = result
            route = []
            for i in range(len(way_points) - 1):
                route.append('{0} -> {1}'.format(way_points[i], way_points[i+1]))
            # The last element in num_passengers is 0
            df = pd.DataFrame({'路線順序': route, '乘客數量': num_passengers[:-1], '時間': durations})
            df.to_excel(writer, sheet_name='路線{0}'.format(route_index))
            route_index += 1

# ori: The number represents the sequence of origin.
# des: The number represents the sequence of destination.
class Car:
    passengers = [] # The keys of origins(destinations).
    waypoints = [] # The list of strings of place names.
    origins = [] # The list of string of origins.
    destinations = [] # The list of string of destinations.
    available_ori = [] # The list of correspoing keys to origins.
    available_des = [] # The list of corresponding keys to destinations.
    durations = []
    num_passengers = []

    def __init__(self, origins, destinations):
        self.passengers = []
        self.waypoints = []
        self.origins = origins
        self.destinations = destinations
        self.available_ori = []
        self.available_des = []
        self.durations = []
        self.num_passengers = []
        for i in range(len(origins)):
            self.available_ori.append(i)
            self.available_des.append(i)
        # Pick a initial start randomly
        init_ori = random.randrange(0, len(origins))
        self.passengers.append(init_ori)
        self.waypoints.append(self.origins[init_ori])
        self.available_ori.remove(init_ori)
        self.num_passengers.append(1)

    def pick_nearst(self, possible_ways, possible_ways_keys):
        current_place = self.waypoints[-1]
        res = gmaps.distance_matrix(origins=current_place, destinations = possible_ways, language='zh-TW', region='tw', mode='driving', units='metric')
        duration_value = []
        for element in res['rows'][0]['elements']:
            duration_value.append(element['duration']['value'])
        # Choose the way with minimum duration
        duration_value = np.asarray(duration_value)
        next_id = np.argmin(duration_value)
        self.durations.append(duration_value[next_id])
        next_key = possible_ways_keys[next_id]
        if next_key['type'] == 'ori':
            # Add an passenger
            self.passengers.append(next_key['key'])
            self.waypoints.append(self.origins[next_key['key']])
            self.available_ori.remove(next_key['key'])
        else:
            # Resolve a passenger
            self.passengers.remove(next_key['key'])
            self.waypoints.append(self.destinations[next_key['key']])
            self.available_des.remove(next_key['key'])
        
    def next_point(self):
        possible_ways = []
        possible_ways_keys = []
        # The car is full.
        if len(self.passengers) > 2:
            for des_key in self.passengers:
                possible_ways_keys.append({'key': des_key, 'type': 'des'})
                possible_ways.append(self.destinations[des_key])
        # The car is empty
        elif len(self.passengers) < 1:
            for ori_key in self.available_ori:
                possible_ways_keys.append({'key': ori_key, 'type': 'ori'})
                possible_ways.append(self.origins[ori_key])
        else:
            for ori_key in self.available_ori:
                possible_ways_keys.append({'key': ori_key, 'type': 'ori'})
                possible_ways.append(self.origins[ori_key])
            for des_key in self.passengers:
                possible_ways_keys.append({'key': des_key, 'type': 'des'})
                possible_ways.append(self.destinations[des_key])
        self.pick_nearst(possible_ways, possible_ways_keys)
        self.num_passengers.append(len(self.passengers))

    def run(self):
        while len(self.available_des) > 0 or len(self.available_ori) > 0:
            self.next_point()
        return (self.waypoints, self.num_passengers, self.durations)
