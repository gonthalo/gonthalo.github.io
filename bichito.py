#comments comments comments
###comments R FAN
"""although I don't Us dem cose aim sach ah bud person"""
import urllib, urllib2
from lxml import html
import re

linkstart = 'href="/wiki/'

def get_html(some_url):
	"""except urllib2.HTTPError, e:print e.fp.read()return 'muymal'"""
	try:
		page = urllib2.urlopen(some_url)
		return page.read()
	except:
		#print 'Los rusos han tratado de detener al crawler. Muy pero que muy mal.'
		return ''
	return page.read()

def get_next_link(page):
	v1 = page.find(linkstart)
	if v1 == -1:
		return False, 0
	#print v1, page[v1:v1 + 45]
	v2 = page.find('"', v1)
	v3 = page.find('"', v2 + 1)
	return page[v2 + 1:v3], v3 + 1


def get_links(page):
	links = []
	while True:
		url, v1 = get_next_link(page)
		if url:
			links.append(url)
			page = page[v1:]
		else:
			break
	return links

def copy(lis):
	return [el for el in lis]

def showlist(lista):
	for el in lista:
		print el

def apariciones(word, text):
	count = 0
	v1 = -len(word)
	while True:
		v1 = text.find(word, v1 + len(word))
		if v1 == -1:
			return count
		count += 1

def buscar(urls, words):
	freqs = []
	for word in words:
		tot = 0
		for url in urls:
			tot += apariciones(word, get_html(url))
		freqs.append(tot)
	return freqs

def crawl_linear(links, maxi, funct):
	tocrawl = copy(links)
	count = 0
	crawled = []
	while count < maxi and tocrawl:
		pagina = get_html(tocrawl[0])
		if pagina != '':
			new_l = funct(pagina)
			crawled.append(tocrawl.pop(0))
			new_l = filter(lambda x: (x not in crawled and x not in tocrawl), new_l)
			tocrawl = tocrawl + new_l
			count += 1
	return crawled


def crawl_depth(links, max_depth, funct):
	tocrawl = copy(links)
	depth = -1
	crawled = []
	last = tocrawl[-1]
	while depth < max_depth and tocrawl:
		pagina = get_html(tocrawl[0])
		if (pagina != ''):
			new_l = funct(pagina)
			crawled.append(tocrawl[0])
			new_l = filter(lambda x: (x not in crawled and x not in tocrawl), new_l)
			tocrawl = tocrawl + new_l
		if tocrawl.pop(0) == last:
			last = tocrawl[-1]
			depth += 1
	return crawled


def easyinput():
	lis = []
	while True:
		word = raw_input()
		if word=='fin de la cita':
			return lis
		lis.append(word)

def start_dir(page):
	for ii in range(1, len(page) - 1):
		if page[ii]=='/':
			if page[ii+1]!='/' and page[ii-1]!='/':
				return page[:ii]


#print crawl_linear(['http://gonthalo.github.io', 'http://github.com/gonthalo'], 10)
#print crawl_linear(['http://www.google.es/'], 10)

def crawl_elpais(starturl):
	linkstart = 'href="http'
	elpais_urls = crawl_linear([starturl], 40, get_links)
	principal = get_html(starturl)
	tree = html.fromstring(principal)
	nice_content = tree.xpath('//a[@title="Ver noticia"]')
	muchas_url = filter(lambda x: get_html(x)!="", [link.get("href") for link in nice_content])
	print muchas_url
	countries = ['Alemania', 'Espa&ntilde;a', 'Francia', 'Italia', 'Grecia', 'Portugal']
	countries += ['Brasil', 'Argentina', 'Chile', 'Ecuador', 'Cuba', 'Venezuela', 'Estados Unidos', 'M&eacute;xico', 'Canad&aacute;']
	countries += ['Rusia', 'India', 'Indonesia', 'China', 'Bangladesh', 'Japon', 'Iraq', 'Ir&aacute;n', 'Australia']
	countries.sort()
	for country in countries:
		uno = buscar(elpais_urls, [country])[0]
		dos = buscar(muchas_url, [country])[0]
		print '\n ' + country, '-'*(20 - len(country)), uno, '_'*(4 - len(str(uno))), dos, '_'*(4 - len(str(dos))),
		if uno!=0:
			print float(dos)/uno,

def freq(page, word):
	count = 0
	pos = page.find(word)
	while pos > 0:
		page = page[pos + 1:]
		pos = page.find(word)
		count += 1
	return count


def crawl_wikipedia(starturl, maxi, keywords, memory = 500):
	linkstart = 'href="/wiki/'
	m_d = start_dir(starturl)
	tocrawl = [[starturl, 0.]]
	count = 0
	crawled = []
	csteps = []
	record = 0
	while count < maxi and tocrawl:
		pagina = get_html(tocrawl[0][0])
		if pagina != '':
			puntos = sum([freq(pagina, word)**0.5 for word in keywords])
			if puntos > record:
				record = puntos
				csteps.append(tocrawl[0][0])
			print puntos, '   ', tocrawl[0][0]
			new_l = [m_d + link for link in list(set(get_links(pagina)))]
			crawled.append(tocrawl.pop(0)[0])
			new_l = filter(lambda x: (x not in crawled and x not in tocrawl), new_l)
			tocrawl = tocrawl + [[el, puntos] for el in new_l]
			tocrawl.sort(key=lambda x: -x[1])
			tocrawl = tocrawl[:memory]
		count += 1
	return crawled, csteps


"""
def isuser(url):
	if url[:20]=="https://twitter.com/":
		if '/' not in url[20:] and "." not in url[20:]:
			return True
	return False

def get_twitter_users(page):
	lis = get_links(page)
	return filter(isuser, lis)

def crawl_twitter(cuenta, n_l):
	lis = crawl_linear(["https://twitter.com/" + cuenta + "/"], n_l, get_links)
	print lis

"""

#crawl_elpais('http://internacional.elpais.com/')
#crawl_elpais('http://www.elpais.com')

wkpage = 'https://es.wikipedia.org/wiki/Arroz_dorado'

results = crawl_wikipedia(wkpage, 200, ['enfermedad', 'virus', 'mixomatosis', 'genetica', 'conejo'])

for kk in results:
	print kk
