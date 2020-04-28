with open("netflix-prize-data/combined_data_4.txt", "r") as file:
	usersRates = {}
	movie = 0
	for line in file:
		line = line.strip()
		if line[-1] is ':':
			movie = int(line[0:-1])
		else:
			user, rate, _ = line.split(",")
			if user not in usersRates:
				usersRates[user] = []
			pair = (movie, int(rate))
			usersRates[user].append(pair)
	print(usersRates)
	file = open("dataParse-04.txt", 'w')
	for setRates in usersRates:
		flat = 0
		for setRates in usersRates[setRates]:
			if flat == 1:
				file.write(", ")
			flat = 1
			file.write(str(setRates))
		file.write("\n")
	file.close()