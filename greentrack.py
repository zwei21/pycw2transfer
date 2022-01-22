import argparse
from tracknaliser import *

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--start", nargs=2, required=True)
	parser.add_argument("--end", nargs=2, required=True)
	parser.add_argument("--verbose", nargs=1, required=False)
	args = parser.parse_args()
	
	start = args.start
	end = args.end
	
	data = query_tracks(start, end, 50, save=False)

	tracks_data = Tracks(data, 300)

	green = tracks_data.greenest()

	if args.verbose is None:
		print("Path:", end="")
		for p in green.route:
			print(p, end=" ")
		print("\n", end="")
	else:
		pass
	print("CO2:", green.co2(), "kg")
	print("Time:",green.time())



