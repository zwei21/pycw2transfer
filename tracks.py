# Dependencies
import numpy as np
from urllib.request import urlopen, Request
import json
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt

####This is the utils file for project####
####Containing all the dependent functions useful####

#----utils of loading----#
def getUrl(start=(0,0), end=(299,299), min_steps_straight=1, max_steps_straight=6, n_tracks=300):
    start_point_x = "start_point_x={start_x}".format(start_x=start[0])
    start_point_y = "&start_point_y={start_y}".format(start_y=start[1])
    end_point_x = "&end_point_x={end_x}".format(end_x=end[0])
    end_point_y = "&end_point_y={end_y}".format(end_y=end[1])
    min_steps_straight = "&min_steps_straight={min_steps_straight}".format(min_steps_straight=min_steps_straight)
    max_steps_straight = "&max_steps_straight={max_steps_straight}".format(max_steps_straight=max_steps_straight)
    n_tracks = "&n_tracks={n_tracks}".format(n_tracks=n_tracks)
    url_head = "http://ucl-rse-with-python.herokuapp.com/road-tracks/tracks/?"
    url = url_head + start_point_x + start_point_y + end_point_x + end_point_y + min_steps_straight + max_steps_straight + n_tracks
    return url

def ReadData(url):
    request = Request(url)
    response = urlopen(request)
    tracksFile = response.read()
    response.close()

    # Decode UTF-8 bytes to Unicode, and convert single quotes
    # to double quotes to make it valid JSON
    tracksFile = tracksFile.decode('utf8').replace("'", '"') # Json
    tracksDict = json.loads(tracksFile)
    
    return tracksDict


##Road properties and their effect
#---Road type effect----#
def roadType(typeStr):
    #???Use sphinx to add comment automactically???
    speedFloat = 0.0
    confFloat = 1.0

    #Conditional blocks
    if typeStr == 'r':
        speedFloat=30; confFloat = 1.40
    elif typeStr == 'l':
        speedFloat = 80; confFloat = 1.0
    elif typeStr == 'm':
        speedFloat = 120; confFloat = 1.25
    else:
        print('Invalid Roda Type')
    
    return speedFloat, confFloat

#---Terrain effect---#
def terrainType(teriStr):
    #???Use sphinx to add comment automactically???
    confFloat = 1.0

    #Conditional blocks
    if teriStr == 'd':
        confFloat = 2.5
    elif teriStr == 'g':
        confFloat = 1.25
    elif teriStr == 'p':
        confFloat = 1.0
    else:
        print('Invalid Terrian Type')
    
    return confFloat

#---Slope effect---#
def slopeRange(slopeFloat):
    #???Use sphinx to add comment automactically???
    confFloat = 1.0
    #Transfer slope to percentage scale
    slopeFloat = slopeFloat * 100

    #Conditional blocks
    if slopeFloat < -6:
        confFloat = 0.16
    elif slopeFloat >= -6 and slopeFloat < -2:
        confFloat = 0.45
    elif slopeFloat >= -2 and slopeFloat < 2:
        confFloat = 1.0
    elif slopeFloat >= 2 and slopeFloat < 6:
        confFloat = 1.3
    elif slopeFloat >= 6 and slopeFloat < 10:
        confFloat = 2.35
    elif slopeFloat >= 10:
        confFloat = 2.90
    else:
        print('Invalid Slope Range')
    return confFloat

#---Calculate Slope---#
def calSlope(elevaInta,elevaIntb,resolFloat):
    #???Use sphinx to add comment automactically???
    #Scale resolution from km to m
    resolFloat = resolFloat * 1000
    slopeFloat = (elevaIntb - elevaInta) / resolFloat
    return slopeFloat

#---Combining all the factors together---#
##--Calculate actual distance--##
'''
Combining the slope effect to the distance
input: slope, resolution
output: distance
'''
def calDistance(slopeFloat, resolution):
    #???Use sphinx to add comment automactically???

    return  resolution * np.sqrt(1+slopeFloat**2)
##--Calculate carbon emission--#
'''
Using actual distance to give carbon emission
input:  avgConsumption
        resolution, Effects(slope, road, terrian), distance
        carbonproduction
output: carbon
'''

def calCons(confRoad, confTeri, confSlope, distance, avgCons=0.054, carbonProd=2.6391):
    #???Use sphinx to add comment automactically???
    distance = distance / 1000

    carbonEmission = avgCons * confRoad * confTeri * confSlope * distance * carbonProd # Unit: kg

    return carbonEmission




#----utils Class----#




def ccReader(start, cc):
    points = [start]
    current = start[:] # Initializing
    for i in range(len(cc)):
        if cc[i] == "1":
            next_step = [current[0] + 1, current[1]]
            points.append(next_step)
            current = next_step
        elif cc[i] == "2":
            next_step = [current[0], current[1] + 1]
            points.append(next_step)
            current = next_step
        elif cc[i] == "3":
            next_step = [current[0] - 1, current[1]]
            points.append(next_step)
            current = next_step
        elif cc[i] == "4":
            next_step = [current[0], current[1] - 1]
            points.append(next_step)
            current = next_step
        else :
            print("Unexpected chaincode value.")
    return points

def TurningPoints_cc(cc):

  new_cc = [[cc[0], '0']]

  for i in range(len(cc)-1):
    if cc[i+1] != cc[i]:
      direction = cc[i+1]
      index = i+1

      new_cc.append([direction,str(index)])

    else:
      pass

  return new_cc


#----Class----#

class SingleTrack():
    
    def __init__(self, tracksDict, index):
        
        self.start = tracksDict['metadata']['start']
        self.end = tracksDict['metadata']['end']
        self.steps = len(tracksDict['tracks'][index]['cc'])
        self.cc = tracksDict['tracks'][index]['cc']
        self.road = tracksDict['tracks'][index]['road']
        self.terrain = tracksDict['tracks'][index]['terrain']
        self.elevation = tracksDict['tracks'][index]['elevation']
        
    def __str__(self):
        return "<SingleTrack: starts at ({x0},{y0}) - {steps} steps>".format(x0=str(self.start[0]),y0=str(self.start[1]), steps = str(self.steps))
    
    def __len__(self):
        return self.steps
    
    def corners(self):
        corners = []
        points = ccReader(self.start, self.cc)
        cornersTuple = TurningPoints_cc(self.cc)
        for i in range(len(cornersTuple)):
            corners.append(points[int(cornersTuple[i][1])])
        corners.append(points[-1])
        return corners
    
    def visualise(self, show = True, filename = "track.png"):
        
        # Default: Show; Not Save
        
        # ---- Plot Figures ----
        plt.figure(figsize=(16,8))
        
        # ---- Figure 1: ----
        elevation = self.elevation
        dist = 0
        distance = [dist]
        for i in range(len(self.cc)):
            slope = calSlope(self.elevation[i], self.elevation[i+1], 1)
            dist += calDistance(slope, 1)
            distance.append(dist)
            
        plt.subplot(1, 2, 1)

        plt.xlabel('distance(km)')
        plt.ylabel('elevation(m)')
        plt.plot(distance,elevation,'r-')

        # ---- Figure 2: ----

        # coordinates:
        coordinates = ccReader(self.start,self.cc)

        x = [row[0] for row in coordinates]
        y = [row[1] for row in coordinates]

        plt.subplot(1, 2, 2)

        plt.xlabel('x(km)')
        plt.ylabel('y(km)')
        plt.suptitle(filename)
        
        for i in range(len(coordinates)):
            plt.plot(x[i:i+2], y[i:i+2], 'r-')
        
        plt.show()
        
        # Check whether show and save .png figure or not
        if show == False:
            plt.savefig(filename)
            plt.close()
        else:
            pass
        
    def co2(self):
        co2 = 0.0
        for i in range(len(self.cc)):
            slope = calSlope(self.elevation[i], self.elevation[i+1], 1)
            _, conf_r = roadType(self.road[i])
            conf_t = terrainType(self.terrain[i])
            conf_s = slopeRange(slope)
            distance = calDistance(slope, 1)
            co2 += calCons(conf_r, conf_t, conf_s, distance)
        return co2
    
    def distance(self):
        distance = 0.0
        for i in range(len(self.cc)):
            slope = calSlope(self.elevation[i], self.elevation[i+1], 1)
            distance += calDistance(slope, 1)
        return distance
    
    def time(self):
        time = 0.0
        for i in range(len(self.cc)):
            slope = calSlope(self.elevation[i], self.elevation[i+1], 1)
            distance = calDistance(slope, 1)
            speed, _ = roadType(self.road[i])
            time += distance / speed
        return time
    
    
    
    
    
#---Tracks---#

#----Define Tracks class----#

class Tracks():

    def __init__(self,rawDict):
        self.tracksDic = rawDict

        self.metadata = self.tracksDic['metadata']
        self.tracks = self.tracksDic['tracks']

        self.datetimeStr = self.metadata['datetime']
        self.date = datetime.strptime(self.datetimeStr, '%Y-%m-%dT%H:%M:%S')
        self.start = self.metadata['start']
        self.end = self.metadata['end']
        self.mapsize = self.metadata['mapsize']
        self.n_tracks = self.metadata['n_tracks']  # len(tracks)
        self.resolution = self.metadata['resolution']
        self.units_elevation = self.metadata['units_elevation']
        self.units_steps = self.metadata['units_steps']
        
        self.track = []
        for i in range(self.n_tracks):
            self.track.append(SingleTrack(self.tracksDic, i))
    # ---------------------
    def __str__(self):
        return("<Tracks: {} from ({}, {}) to ({},{})>".format(self.n_tracks, self.start[0], self.start[1], self.end[0], self.end[1]))
    
    def greenest(self):
        
        # Initialisation
        tracks_co2 = []
        
        # co2:
        for i in range(len(self.tracks)):
 
            a_track = SingleTrack(self.tracksDic, i)
            co2 = a_track.co2()
            tracks_co2.append(co2)
        
        # get the greenest index
        index = tracks_co2.index(np.min(tracks_co2))
        
        # greenest object
        greenest_track = self.get_track(index)
        
        return greenest_track
        
    def fastest(self):
        
        # Initialisation
        tracks_time = []
        
        # time:
        for i in range(len(self.tracks)):
 
            a_track = SingleTrack(self.tracksDic, i)
            time = a_track.time()
            tracks_time.append(time)
        
        # get the fastest index
        index = tracks_time.index(np.min(tracks_time))
        
        # fastest object
        fastest_track = self.get_track(index)
        
        return fastest_track
        
    def shortest(self):
       
        # Initialisation
        tracks_distance = []
        
        # time:
        for i in range(len(self.tracks)):
 
            a_track = SingleTrack(self.tracksDic, i)
            distance = a_track.distance()
            tracks_distance.append(distance)
        
        # get the fastest index
        index = tracks_distance.index(np.min(tracks_distance))
        
        # fastest object
        shortest_track = self.get_track(index)
        
        return shortest_track
    
    # -- clustering --
    
    def kmeans():
        
        return 0
    
    def get_track(self, x):
        #assert x < len(tracks)
        
        return self.track[x]
        