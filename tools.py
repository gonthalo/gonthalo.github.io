
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

nim = Game(nim_next, nim_moves, nim_util, ([1, 3, 5, 7], 1), nim_show)


nim.show()
nim.play((2, 3))
nim.show()

nim_strat = Minymax(nim_next, nim_moves, nim_util)
print nim_strat.best([2, 5, 0], 1)
print nim_strat.u(([2, 5, 0], 1), 1)
print nim_strat.m([2, 5, 0], 1)
print nim_strat.u(([2, 2, 0], 0), 1)