import sys
import time
import zmq
import json
import linecache
import math
import matplotlib.pyplot as plt

storage = {}

def getBounds(arr):
	if len(arr) > 1:
		first = arr[0]
		first = int(first[1:len(first)].split(",")[0])
		last = arr[len(arr) - 1]
		last = int(last[0:len(last) - 2].split(",")[0])
	else:
		first = arr[0].split(",")
		first = int(first[0][1:])
		last = first
	return (first, last)

def graphStats(nameFile, option):
	first_movie = 1000000
	last_movie = 0

	with open(nameFile) as file:
		it = 0
		for line in file:
			it += 1
			split_line = line.split("), (")
			key = len(split_line)
			bounds = getBounds(split_line)
			first_movie = min(bounds[0], first_movie)
			last_movie = max(bounds[1], last_movie)
			if key in storage.keys():
				storage[key] = storage[key] + 1
			else:
				storage[key] = 1

	print(f"Data from {first_movie} to {last_movie}")

	for key in sorted(storage.keys()):
		print(f"{ storage[key] * 100 / it  }% look {key} movies")

	plt.scatter(*zip(*storage.items()))
	plt.show()

graphStats(sys.argv[1])