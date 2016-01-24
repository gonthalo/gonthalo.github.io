import random
import math
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt

def gen(n, start, nit):
	lis = [start for ii in range(n)]
	for ii in range(nit):
		rand = random.randint(1, sum(lis))
		for jj in range(n):
			if sum(lis[:jj + 1])>=rand:
				lis[jj] += 1
				break
		lis.sort()
	return lis

def pinta(listas):
	tot = len(listas[0])
	for lista in listas:
		for ii in range(tot):
			plt.scatter(ii, lista[ii], color='b')
	plt.show()
	medias = [sum(lista[ii] for lista in listas)/(len(listas) + 0.0) for ii in range(tot)]
	print medias
	for ii in range(tot):
		plt.scatter(tot - ii, medias[ii], color='k')
	plt.show()
	for ii in range(tot):
		plt.scatter(math.log(tot - ii), math.log(medias[ii]), color='k')
	plt.show()
comb = []

for kk in range(200):
	new_l = gen(15, 1, 750)
	print new_l
	comb.append(new_l)

pinta(comb)
