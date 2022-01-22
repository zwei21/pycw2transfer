import matplotlib.pyplot as plt
import math
import numpy as np

freeman_cc2coord = {
	1: [1, 0],
	2: [0, 1],
	3: [-1, 0],
	4: [0, -1],
}

road_type = {
	'r': [30.0, 1.4],
	'l': [80.0, 1.0],
	'm': [120.0, 1.25]
}

terrain = {
	'd': 2.5, 
	'g': 1.25,
	'p': 1.0
}

slope = {
	-8: 0.16,
	-4: 0.45,
	0: 1,
	4: 1.3,
	8: 2.35,
	12: 2.90
}

class SingleTrack:
	def __init__(self, metadata, track):
		self.start = metadata['start']
		self.end = metadata['end']
		self.cc = track['cc']
		self.road = track['road']
		self.terrain = track['terrain']
		self.eval = track["elevation"]

		self.route = []
		def route_cc():
			self.route.append(self.start)
			for c in self.cc:
				self.route.append(np.array(freeman_cc2coord[int(c)]) + np.array(self.route[-1]))
		route_cc()



	def len(self):
		return len(self.route)
	
	def corners(self):
		cor = set()
		if self.start != self.end:
			cor.add(tuple(self.start))
			cor.add(tuple(self.end))
		for i in range(1, len(self.cc)):
			if (int(self.cc[i - 1]) + int(self.cc[i])) % 2 != 0:
				cor.add(tuple(self.route[i]))

		return list(cor)
	
	def visualise(self, show=True, filename="my_track.png"):
		plt.subplot(1, 2, 1)
		plt.plot(range(len(self.eval)), self.eval)
		plt.subplot(1, 2, 2)
		x = [ p[0] for p in self.route]
		y = [ p[1] for p in self.route]
		plt.plot(x, y)

		if show:
			plt.show()
		else:
			plt.savefig(filename)


	def distance(self):
		d = 0
		for e in self.eval:
			d += math.sqrt(1 + (e / 100)**2)
		return d

	def time(self):
		t = 0.0
		for r in self.road:
			t += 1.0 / road_type[r][0]
		return t

	def co2(self):
		emit = 0.0
		for i in range(len(self.road)):
			sl = np.array(list(slope.keys())) - self.eval[i]
			emit += 5.4 / 100 * slope[list(slope.keys())[sl.argmin()]] * \
				road_type[self.road[i]][1] * terrain[self.terrain[i]] * \
					math.sqrt(1 + (self.eval[i] / 100)**2) * 1000 * 2.6391
		return emit

	def __str__(self):
		return("<SingleTrack: starts at ({},{}) - {} steps>".format(self.start[0], self.start[1], len(self.cc)))


#test = SingleTrack({"datetime":"2021-12-11T21:12:20","end":[4,2],"mapsize":[5,5],"n_tracks":5,"rangesteps":[1,2],"resolution":1,"start":[2,3],"units_elevation":"m","units_steps":"km"},{"cc":"11233344111","elevation":[17,18,19,24,23,22,21,16,11,12,13,14],"road":"llmmmmlrrrr","terrain":"pggppdddppg"})
#print(test)
#print(test.co2())
#print(test.time())
#print(test.len())
#test.visualise()
#print(test.corners())

class Tracks:
	def __init__(self, data, map_size):
		self.metadata = data["metadata"]
		self.tracks = []
		for track in data["tracks"]:
			atrack = SingleTrack(self.metadata, track)
			if(np.max(np.array(atrack.route)) >= map_size or np.min(np.array(atrack.route)) < 0):
				continue
			self.tracks.append(atrack)

		self.start = self.metadata["start"]
		self.end = self.metadata["end"]
		self.map_size = map_size
		self.date = self.metadata["datetime"]

	def len(self):
		return len(self.tracks)
	
	def greenest(self):
		minco2 = float("inf")
		argmin = None
		for t in self.tracks:
			if t.co2() < minco2:
				minco2 = t.co2()
				argmin = t
		return argmin

	def fastest(self):
		mintime = float("inf")
		argmin = None
		for t in self.tracks:
			if t.time() < mintime:
				mintime = t.time()
				argmin = t
		return argmin

	def shortest(self):
		mindis = float("inf")
		argmin = None
		for t in self.tracks:
			dist = t.distance()
			if dist < mindis:
				mindis = dist
				argmin = t
		return argmin

	def get_track(self, x):
		return self.tracks[x]

	def __str__(self):
		return("<Tracks: {} from ({}, {}) to ({},{})>".format(self.len(), self.start[0], self.start[1],  self.end[0], self.end[1]))

	def kmeans(self, clusters=3, iterations=10):
		pass ##TODO

