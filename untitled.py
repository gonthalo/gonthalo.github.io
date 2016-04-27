alf = 'zyxwvutsrqponmlkjihgfedcba ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def parsematr(matr):
	for ii in range(len(matr)):
		for jj in range(len(matr[0])):
			matr[ii][jj] = alf.index(matr[ii][jj]) - 26
	return matr
print parsematr([['a', 'B'], ['r', 'W']])

def getsum(matr, p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	tot = 0
	for ii in range(x1, x2 + 1):
		for jj in range(y1, y2 + 1):
			tot += matr[ii%len(matr)][jj%len(matr[0])]
	return tot

def getmax(matr):
	for line in matr:
		if sum(line)>0:
			return 'INFINITY'
	colsums = [0]*len(matr[0])
	for ii in range(len(matr[0])):
		for jj in range(len(matr)):
			colsums[jj] += matr[jj][ii]
	for el in colsums:
		if el>0:
			return 'INFINITY'
	maxi = max(map(lambda x: max(x), matr))
	if maxi == 0:
		return '0'
	record = 0
	for ii in range(len(matr)):
		for jj in range(len(matr[0])):
			for iii in range(len(matr)):
				for jjj in range(len(matr[0])):
					tt = getsum(matr, (ii, jj), (ii + iii, jj + jjj))
					if tt>record:
						record = tt
	return str(record)

print getmax([[0, 0, -1], [1, -1, 0], [-2, 1, 1]])
