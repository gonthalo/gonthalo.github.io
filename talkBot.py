
from random import random

nombres = ['sombrero', 'papel', 'programa', 'hombre', 'tiempo']
verbos_t = ['se come', 'atraviesa', 'es', 'teni\xc3a']
verbos_i = ['piensa', 'se rompe', 'escucha']
adjets = ['naranja', 'curioso', 'feliz', 'malo']
advers = ['muy', 'demasiado']
prepos = ['de', 'por', 'en']
deters = ['un', 'el', 'su']

mayu = 'QWERTYUIOPLKJHGFDSAZXCVBNM'
minu = 'qwertyuioplkjhgfdsazxcvbnm'

def randatr():
	return getrand([True, False]), getrand([True, False])

def getrand(lista):
	r = int(random()*len(lista))
	return lista[r]

def procesar(strin):
	ans = ""
	for ii in strin:
		if ii=='\n':
			ans += " "
		elif ii=='.' or ii==',' or ii==':':
			ans += " " + ii
		elif ii in mayu:
			ans += minu[mayu.index(ii)]
		else:
			ans += ii
	return ans.split(' ')

def convertir(mierda):
	prov = ''
	prev = '.'
	for el in mierda:
		if el in ['.', ',', ':', '']:
			prov += el
		else:
			if prev == '.' and el[0] in minu:
				el = mayu[minu.index(el[0])] + el[1:]
			prov += ' ' + el
		prev = el
	prov = prov.replace(' de el ', ' del ')
	prov = prov.replace(' a el ', ' al ')
	return "=" + prov

def analisis_frecuencias(camino):
	archivo = open(camino, 'r')
	coleccion = reduce(lambda x, y: x + y, [procesar(line) for line in archivo.readlines()])
	indice = list(set(coleccion))
	freq = [0 for ii in range(len(indice))]
	for elem in coleccion:
		freq[indice.index(elem)] += 1
	return sorted(indice, key=lambda x: 0 - freq[indice.index(x)])

#SINTAXIS

def s_adj(gen, num, dep):
	ans = [getrand(adjets)]
	if dep==0:
		return ans
	if random()*4 < 1:
		ans = [getrand(advers)] + ans
	return ans

def s_nom(gen, num, dep):
	if dep==0:
		if 2*random()>0: #usually 1
			return [getrand(deters), getrand(nombres)]
		return [getrand(nombres)]
	ans = s_nom(gen, num, dep - 1)
	if 3*random()<1:
		ans = ans + s_adj(gen, num, dep - 1)
	if 3*random()>1:
		ans = ans + [getrand(prepos)] + s_nom(gen, num, dep - 1)
	return ans

def pred(gen, num, dep):
	if dep==0:
		return [getrand(verbos_i)]
	if random()*2>1:
		ans = [getrand(verbos_i)]
	else:
		aux1, aux2 = randatr()
		ans = [getrand(verbos_t)] + s_nom(aux1, aux2, dep - 1)
	return ans

def frase(dep):
	gen, num = randatr()
	return s_nom(gen, num, dep - 1) + pred(gen, num, dep - 1) + ['.']


print convertir(frase(3))
#print convertir(analisis_frecuencias('/home/gonthalo/Desktop/text_sample.txt')[:100])
