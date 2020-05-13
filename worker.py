# Task worker
# Connects PULL socket to tcp://localhost:5557
# Collects workloads from ventilator via that socket
# Connects PUSH socket to tcp://localhost:5558
# Sends results to sink via that socket
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import sys
import time
import zmq
import json
import linecache
import math

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

def norm(u):
	''' Recibe un vector disperso y calcula su norma'''
	ans = 0
	for comp in u:
			ans += comp[1]**2
	return math.sqrt(ans)

def dotProd(u,v):
	''' Recibe dos vectores dispersos y calcula el producto punto'''
	i = j = 0
	ans = 0
	c = 13000
	while i < len(v) and j < len(u):
			if (v[i][0] - c) == u[j][0]:
					ans += ( v[i][1] * u[j][1] )
					i += 1
					j += 1
			elif (v[i][0] - c) < u[j][0]:
					i += 1
			else:
					j += 1
	return ans

def arc(u,v, normu):
	''' Recibe dos vectores dispersos y calcula su angulo '''
	dot = dotProd(u,v)
	ans = math.acos(dot / (normu * norm(v)))
	print(normu)
	return ((ans)* 180) / math.pi

def distance(pointA,pointB):
	return sum([ (x[0] - x[1])**2 for x in zip(pointA, pointB) ])

def getPoint(line):
	return [float(x) for x in line.split(",")]

def getValues(points):
	values = points.split(", ")
	return (int(values[0]) - 1, int(values[1]))

def getCustomer(line):
	arr = line.split("), (")
	aux = arr[0]
	aux = aux[1:len(aux)]
	arr.pop(0)
	arr.insert(0,aux)
	aux = arr[len(arr) - 1]
	aux = aux[0:len(aux) - 2]
	arr.pop(len(arr) - 1)
	arr.append(aux)
	return [ getValues(pair) for pair in arr]

def disperse(u):
	return [ (i, x) for i, x in enumerate(u)]

def calculateDistance(id, centroids, nameFile, norms):
	return [arc(disperse(centroid), getCustomer(linecache.getline(nameFile, id + 1)), norms[i]) for i,centroid in enumerate(centroids)] 

def emptyList(dimension):
	return [0 for i in range(dimension)]

# Process tasks forever
while True:
	nameFile = "./netflix-prize-data/dataTest.txt"
	c = 13000
	tasks = json.loads(receiver.recv())
	
	data = {"tags":[], "sums":[ emptyList(len(tasks["centroids"][0])) for i in range(len(tasks["centroids"]))], "inertia": 0}

	inertia = 0

	for id in range(tasks["range"][0], tasks["range"][1]):
		distances = calculateDistance(id, tasks["centroids"],nameFile,tasks["norms"])
		data["tags"].append([id, distances[0], 0])
		
		for i,value in enumerate(distances):
			if value < data["tags"][len(data["tags"]) - 1][1]:
				data["tags"][len(data["tags"]) - 1] = [id,value,i]
		
		currentPoint = getCustomer(linecache.getline(nameFile, id + 1))
		j = 0
		for i in range(len(tasks["centroids"][0])):
			tag = data["tags"][len(data["tags"]) - 1][2]
			if j < len(currentPoint):
				if currentPoint[j][0] == (i + c):
					data["sums"][tag][i] += currentPoint[j][1]
					inertia += (currentPoint[j][1] - tasks["centroids"][tag][i])**2
					j += 1
	data["inertia"] = inertia
	sender.send_string(json.dumps(data))

