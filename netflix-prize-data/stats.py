import sys
import time
import zmq
import json
import linecache
import math
import matplotlib.pyplot as plt

storage = {}
movies = {}

def getValues(points):
	values = points.split(", ")
	return (int(values[0]) - 1, int(values[1]))

def getCustomer(arr):
	if len(arr) > 1:
		aux = arr[0]
		aux = aux[1:len(aux)]
		arr.pop(0)
		arr.insert(0,aux)
		aux = arr[len(arr) - 1]
		aux = aux[0:len(aux) - 2]
		arr.pop(len(arr) - 1)
		arr.append(aux)
	else:
		arr[0] = arr[0][1:-2]
	return [ getValues(pair) for pair in arr]

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

def graphStats(nameFile, option="reset"):
	first_movie = 1000000
	last_movie = 0

	with open(nameFile) as file:
		it = 0
		for line in file:
			it += 1
			split_line = line.split("), (")
			key = len(split_line)
			bounds = getBounds(split_line)
			if key > 100 and key < 170:
				print(line[:-1])
			first_movie = min(bounds[0], first_movie)
			last_movie = max(bounds[1], last_movie)
			if key in storage.keys():
				storage[key] = storage[key] + 1
			else:
				storage[key] = 1
			for pair in getCustomer(split_line):
				if pair[0] in movies:
					movies[pair[0]] += 1
				else:
					movies[pair[0]] = 1

	if option == "reset":
		print(f"Data from {first_movie} to {last_movie}")
		for key in sorted(storage.keys()):
			print(f"{ storage[key] * 100 / it  }% look {key} movies")

	print(*reversed(sorted(movies.items())))
	print(f"{it / 4800}% of the customers look movie from {first_movie} to {last_movie}")
	plt.scatter(*zip(*storage.items()))
	plt.show()

graphStats(sys.argv[1], sys.argv[2])