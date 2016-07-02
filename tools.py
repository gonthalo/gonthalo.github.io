
def dikjistra(start, conex, target):
	"""
	Calcula la distancia entre dos vertices de un grafo
	Start y Target son los vertices cuya distancia se quiere calcular
	Conex es el grafo representado como lista de tuplas (v_i, v_j, d(v_i, v_j))
	"""
	ind = list(set([con[0] for con in conex] + [con[1] for con in conex]))
	t = len(ind)
	maxi = sum([con[2] for con in conex])
	dist = [maxi for ii in range(t)]
	check = [0 for ii in range(t)]
	dist[ind.index(start)]=0
	#print 'INDEX: ', ind
	while True:
		mini = maxi + 1
		pos = -1
		for ii in range(t):
			if (dist[ii]<mini and check[ii]==0):
				pos = ii
				mini = dist[ii]
		if (pos == -1):
			return False
		if ind[pos] == target:
			return dist[pos]
		for aa, bb, dd in conex:
			aaa, bbb = ind.index(aa), ind.index(bb)
			if aaa==pos and check[bbb]==0:
				dist[bbb] = min(dist[bbb], dist[pos] + dd)
			if bbb==pos and check[aaa]==0:
				dist[aaa] = min(dist[aaa], dist[pos] + dd)
		check[pos] = 1
		#print 'Vert, ', ind[pos], 'Distances, ', dist


"""Funcion de expansion binaria"""


def binfunc(n, par, impar, args):
	def f(x):
		if n%2:
			return impar((x-1)/2, f, args)
		else:
			return par(x/2, f, args)
	return f(n)

def evenexp(k, expf, args):
	base, mod = args
	if k==0:
		return 1
	return (expf(k)*expf(k))%mod

def oddexp(k, expf, args):
	base, mod = args
	if k==0:
		return base
	return (expf(k)*expf(k)*base)%mod

#print binfunc(12, evenexp, oddexp, (5, 13))

def expon(base, ex, mod):
	return binfunc(ex, evenexp, oddexp, (base, mod))


"""T. de Numeros"""

def primos_hasta(num):
	lista = [2, 3]
	n = 5
	while n < num:
		for div in lista:
			if n%div == 0:
				break
			if div*div > n:
				lista.append(n)
				break
		n += 1
	return lista


"""Minimax y T. de Juegos"""


class Game:
	def __init__(self, next, moves, util, start, show):
		self.state, self.turn = start
		self.m = moves
		self.n = next
		self.ut = util
		self.show_st = show
	def show(self):
		self.show_st(self.state)
	def play(self, move):
		if move in self.m(self.state, self.turn):
			self.state, self.turn = self.n(self.state, move, self.turn)

class Minymax:
	def __init__(self, next, moves, util):
		self.n = next
		self.m = moves
		self.ut = util
	def best(self, state, player):
		rec, good = None, None
		for move in self.m(state, player):
			aa, bb = self.n(state, move, player)
			if self.ut(aa, bb, player)==1:
				return move
		for move in self.m(state, player):
			value = self.u(self.n(state, move, player), player)
			if rec==None or value>rec:
				value = rec
				good = move
		return good
	def u(self, args, player):
		state, turn = args
		if self.ut(state, turn, player)!=None:
			return self.ut(state, turn, player)
		nextm = self.best(state, turn)
		return self.u(self.n(state, nextm, turn), player)


#Juego del NIM
def nim_moves(state, turn):
	return reduce(lambda x, y: x + y, [[(ii, jj) for jj in range(1, state[ii] + 1)] for ii in range(len(state))])

def nim_next(state, move, player):
	ind, nn = move
	nstate = [el for el in state]
	nstate[ind] -= nn
	return (nstate, 1 - player)

def nim_util(state, turn, player):
	if sum(state)==0:
		return 1 - (player==turn)
	return None

def nim_show(state):
	for ii in state:
		print 'I'*ii
'''
nim = Game(nim_next, nim_moves, nim_util, ([1, 3, 5, 7], 1), nim_show)


nim.show()
nim.play((2, 3))
nim.show()

nim_strat = Minymax(nim_next, nim_moves, nim_util)
print nim_strat.best([2, 5, 0], 1)
print nim_strat.u(([2, 5, 0], 1), 1)
print nim_strat.m([2, 5, 0], 1)
print nim_strat.u(([2, 2, 0], 0), 1)
'''

"""Biblioteca de polinomios"""

def p_str(num):
	if num < 0:
		return str(num)
	return '+' + str(num)

class Polinomio:
	def __init__(self, lista, var, anulador=None, cer0=0):
		self.coef = lista
		self.grado = len(lista) - 1
		self.var = var
		self.anul = anulador
		self.cer0 = cer0
	def eval(self, x):
		return sum([self.coef[ii]*(x**ii) for ii in range(self.grado + 1)])
	def __add__(self, other):
		s1 = self.coef
		s2 = other.coef
		if len(s1) > len(s2):
			s1, s2 = s2, s1
		for ii in range(len(s1)):
			s2[ii] += s1[ii]
		return Polinomio(s2, self.var, anulador = self.anul, cer0 = self.cer0)
	def __mul__(self, other):
		nlista = [self.cer0]*(self.grado + other.grado + 1)
		for ii in range(self.grado + 1):
			for jj in range(other.grado + 1):
				nlista[ii + jj] += self.coef[ii]*other.coef[jj]
		npoli = Polinomio(nlista, self.var, anulador = self.anul, cer0 = self.cer0)
		if self.anul == None:
			return npoli
		return npoli%self.anul
	def __str__(self):
		if self.coef == [0]*(self.grado + 1):
			return '0'
		rep = p_str(self.coef[0])*(self.coef[0] != 0)
		if self.grado > 0 and self.coef[1] != 0:
			cc = p_str(self.coef[1])
			if cc == '+1':
				cc = '+'
			if cc == '-1':
				cc = '-'
			rep = cc + self.var + ' ' + rep
		for ii in range(2, self.grado + 1):
			if self.coef[ii] != 0:
				cc = p_str(self.coef[ii])
				if cc == '+1':
					cc = '+'
				if cc == '-1':
					cc = '-'
				rep = cc + self.var + '^' + str(ii) + ' ' + rep
		return rep
	def __div__(self, other):
		lD = [ee for ee in self.coef]
		ld = [ee for ee in other.coef]
		alfa = ld[other.grado]
		lQ = []
		for ii in range(1 + self.grado - other.grado):
			beta = lD[self.grado - ii]/alfa
			for jj in range(other.grado):
				lD[self.grado - other.grado - ii + jj] -= beta*ld[jj]
			lQ = [beta] + lQ
		return Polinomio(lQ, self.var, anulador = self.anul, cer0 = self.cer0), Polinomio(lD[:other.grado], self.var, anulador = self.anul, cer0 = self.cer0)
	def __mod__(self, other):
		return (self/other)[1]
	def __floordiv__(self, other):
		return (self/other)[0]
	def deriv(self):
		return Polinomio([self.coef[ii + 1]*(ii + 1) for ii in range(self.grado)], self.var, anulador = self.anul, cer0 = self.cer0)
	def escalar(self, meta):
		if meta==0:
			return self.coef[0]
		lis = [num.escalar(meta - 1) for num in self.coef]
		if self.anul == None:
			return Polinomio(lis, self.var, cer0 = self.cer0.escalar(meta - 1))
		return Polinomio(lis, self.var, anulador = self.anul.escalar(meta), cer0 = self.cer0.escalar(meta - 1))
	def newton(self, start):
		xx = start
		dpdx = self.deriv()
		cc = 0
		while abs(self.eval(xx)) > 0.00001:
			xx = xx + self.eval(xx)/dpdx.eval(xx)
			cc += 1
			if cc > 50:
				return None
		return xx
	def root(self, a, b):
		if self.eval(a)*self.eval(b) > 0:
			return None
		if self.eval(b) < 0:
			a, b = b, a
		cc = (a + b)/2.
		while abs(b - a) > 0.0001:
			if self.eval(cc) > 0:
				b = cc
			else:
				a = cc
			cc = (a + b)/2
		return cc
	def raices(self, a, b):
		if self.grado == 1:
			return [-1.*self.coef[0]/self.coef[1]]
		part = [a] + self.deriv().raices(a, b) + [b]
		return filter(lambda x: x!=None, [self.root(part[ii], part[ii + 1]) for ii in range(len(part) - 1)])



p1 = Polinomio([-1, 0, 1], 'x')
p2 = Polinomio([1, 0, 1], 'x')
print p1
print p2*p1
p3 = Polinomio([-1, 2, -3, 3, -2, 1], 'x')
print p3
cociente, resto = p3/p1
print cociente, '     :    ', resto
print p3%p2

char5 = Polinomio([1, 1, 1, 1, 1], 'w')
root1 = Polinomio([0, 1, 0, 0, 1], 'w', anulador = char5)
root2 = Polinomio([0, 0, 1, 1], 'w', anulador = char5)
print root1, ';', root2
print root1*root2

#ahora viene la horrible parte META ideada por el espiritu de ARI

aa, bb, cc = Polinomio([-1, 1], 'y'), Polinomio([3], 'y'), Polinomio([0, 1], 'y')
print aa, ';', bb, ';', cc
meta1 = Polinomio([aa, bb, cc], 'x', cer0 = Polinomio([0], 'y'))
print meta1
print meta1*meta1

def polichachi(n):
	charN = Polinomio([1]*n, 'w')
	uno = Polinomio([1], 'w', anulador = charN)
	cero = Polinomio([0], 'w', anulador = charN)
	prod = Polinomio([uno], 'x', cer0 = cero)
	for ii in range((n-1)/2):
		lis = [0]*n
		lis[ii + 1] = -1
		lis[n - ii - 1] = -1
		rootii = Polinomio(lis, 'w', anulador = charN, cer0 = cero)
		fac = Polinomio([rootii, uno], 'x')
		prod = prod*fac
	return prod

print polichachi(5)
print polichachi(7)
print polichachi(9)
lamda = polichachi(11).escalar(1)
print lamda
print lamda.deriv().deriv().deriv()
print lamda.eval(1)
print lamda.raices(-2., 2.)
print lamda.root(-2., 2.)

def teorema(n):
	poliN = polichachi(n)
	poliN = poliN.escalar(1)
	lis = poliN.raices(-2., 2.)
	print len(lis), 'raices de', (n - 1)/2
	#return len(lis)==(n - 1)/2

for tt in primos_hasta(80)[1:]:
	print 'Para n=' + str(tt) + ' hay', teorema(tt)
