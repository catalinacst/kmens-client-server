import zmq
import random
import time
import json
import random
import math

try:
    raw_input
except NameError:
    # Python 3
    raw_input = input

context = zmq.Context()

# Socket to send messages on
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

# Socket with direct access to the sink: used to synchronize start of batch
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

sinkRep = context.socket(zmq.REP)
sinkRep.bind("tcp://*:5559")

print("Input the number start and end  number of centroids when the workers are ready: ")
start = raw_input()
end = raw_input()
print("Sending tasks to workers…")

numberPoints = 205
dimensions = 5000 #  17770
intervals = 10

def generateCentroid(start, end, size):
	return [ random.randint(start, end) for i in range(size)]

def readFile(nameFile):
	with open(nameFile) as file:
		for i,line in enumerate(file):
			print([float(x) for x in line.split(",")])

def mapper(value, maximum, lenRange):
	return [value, min(maximum, value + lenRange)]

def norm(u):
	''' Recibe un vector disperso y calcula su norma'''
	ans = 0
	for comp in u:
			ans += comp**2
	return math.sqrt(ans)

def getNorm(centroids):
	return [ norm(centroid) for centroid in centroids ]

def work(sizeData, numberIntervals, centroids):
	lenRange = math.ceil(sizeData / numberIntervals)
	rangeWork = [mapper(x,sizeData,lenRange) for x in range(0,sizeData,lenRange)]
	for work in rangeWork:
		task = { "centroids": centroids, "range": work, "norms": getNorm(centroids)}
		sender.send_string(json.dumps(task))

def distance(m, b, x, y):
	return abs(m * x - y + b) / math.sqrt(0.5**2 + 1)

def search(start, end):
	x1 = int(start)
	x2 = int(end)
	y1 = kmeans(start)
	y2 = kmeans(end)
	m = (y2 - y1) / (x2 - x1)
	b = y1 - m * x1
	while(x2 - x1 > 3):
		midleft = x1 + int((x2 - x1) / 3)
		midright = x2 - int((x2 - x1) / 3)
		distanceOne = distance(m,b,midleft, kmeans(midleft))
		distanceTwo = distance(m,b,midright, kmeans(midright))
		if(distanceOne > distanceTwo):
			x2 = midright
		else:
			x1 = midleft
	return x1 + 1

def kmeans(numberCentroids):
	# The first message is "0" and signals start of batch
	sink.send_string(json.dumps([numberCentroids,dimensions, numberPoints]))
	print("Current batch is to k = {}".format(numberCentroids))
	numberIterations = 0
	work(numberPoints,intervals, [ generateCentroid(1 , 5, dimensions) for i in range(int(numberCentroids))])
	numberIterations += 1

	inertia = 0
	while numberIterations < 10:
		print(numberIterations)
		request = sinkRep.recv()
		data =  json.loads(request)
		print(data["inertia"])
		inertia = data["inertia"]
		centroids = data["centroids"]
		sinkRep.send_string('ok')
		work(numberPoints,intervals,centroids)
		numberIterations += 1
	sinkRep.recv()
	sinkRep.send_string('ok')
	print(inertia)
	print("===(finish current batch)===")
	return float(inertia)

print(search(start, end))