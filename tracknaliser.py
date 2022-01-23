import datetime as dt
from tracks import *

#---utils---#
def float2time(float):
    print("Time :", dt.timedelta(hours=float))

def get_turn(now, next):
    # Casting
    now = int(now)
    next = int(next)
    # Exceptions
    if now == 1 and next == 4:
        return 0 # Turn right
    elif now == 4 and next == 1:
        return 1 # Turn left
    else:
        if (next-now) == -1:
            return 0 # Turn right
        elif(next-now) == 1:
            return 1 # Turn left
    
direction_dict = {
    1 : "east",
    2 : "north",
    3 : "west",
    4 : "south"
}

def quedemap(route, corners):
    # Start:
    str_start = "- Start from" + str(corners[0]) 
    print(str_start)

    # Direction and Turns
    for i in range(len(route)-1):
        
        # Direction and Distance
        direction = direction_dict[int(route[i][0])]
        distance = np.linalg.norm(np.array(corners[i]) - np.array(corners[i+1]))

        str_direction = "- Go {dire} for {dist} km,".format(dire=direction,dist=distance)

        # Turn
        if get_turn(route[i][0], route[i+1][0]):
            str_turn = "turn left at {}".format(corners[i+1])
        else:
            str_turn = "turn right at {}".format(corners[i+1])

        print(str_direction, str_turn)

    # End:

    # Direction and Distance
    direction = direction_dict[int(route[-1][0])]
    distance = np.linalg.norm(np.array(corners[-1]) - np.array(corners[-2]))

    str_direction_end = "- Go {dire} for {dist} km,".format(dire=direction,dist=distance)

    print(str_direction_end, "\n- reach your estination at",corners[-1])
    
#----Functions to be load in main----#
def load_tracksfile(file_path):
    
    #Instantiated Tracks object and read the data.
    with open(file_path) as jsonFile:
        #Open local .json file as instance in Python.
        rawDict = json.load(jsonFile)
        tracks = Tracks(rawDict)
    
    return tracks

def query_tracks(start=(0,0), end=(299,299), min_steps_straight=1, max_steps_straight=6, n_tracks=300,save=False):
    url = getUrl(start, end, min_steps_straight, max_steps_straight, n_tracks)
    
    #Read the data and save as an object.
    rawDict = ReadData(url)
    tracks = Tracks(rawDict)
    
    # File name generator:
    dateStr = tracks.datetimeStr.replace("-", "").replace(":", "")
    startStr = str(start).replace(",","_").replace(" ", "").replace("(","").replace(")","")
    endStr = str(end).replace(",","_").replace(" ", "").replace("(","").replace(")","")
    
    fileName = "tracks_{date}_{n_tracks}_{start}_{end}.json".format(date=dateStr, n_tracks=n_tracks,\
                                                                    start=startStr, end=endStr)
    
    if save == True:
        temp = json.dumps(tracks.tracksDic)
        temp_a = open(fileName, 'w')
        temp_a.write(temp)
        temp_a.close
    else:
        pass
        
    return tracks