import argparse
from tracknaliser import *

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--start", nargs=2, required=True)
	parser.add_argument("--end", nargs=2, required=True)
	parser.add_argument('-v', '--verbose', action="count", 
                        help="increase output verbosity (e.g., -vv is more than -v)")
	args = parser.parse_args()
	
	start = args.start
	end = args.end
	
	tracks = query_tracks(start, end, n_tracks=50, save=False)

	green = tracks.greenest()
	route = TurningPoints_cc(green.cc)
	corners = green.corners()

	if args.verbose is None:
		print("Path:", end="")
		for p in green.corners():
			print(p, end=" ")
		print("\n", end="")
	else:
		quedemap(route, corners)
	print("CO2:", green.co2(), "kg")
	float2time(green.time())



