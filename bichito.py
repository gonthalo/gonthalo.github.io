#comments comments comments
###comments R FAN
"""although I don't Us dem cose aim sach ah bud person"""
import urllib, urllib2
from lxml import html

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
	v1 = page.find('<a href="http')
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

def crawl_linear(links, maxi):
	tocrawl = copy(links)
	count = 0
	crawled = []
	while count < maxi and tocrawl:
		pagina = get_html(tocrawl[0])
		if pagina != '':
			new_l = get_links(pagina)
			crawled.append(tocrawl.pop(0))
			new_l = filter(lambda x: (x not in crawled and x not in tocrawl), new_l)
			tocrawl = tocrawl + new_l
			count += 1
	return crawled


def crawl_depth(links, max_depth):
	tocrawl = copy(links)
	depth = -1
	crawled = []
	last = tocrawl[-1]
	while depth < max_depth and tocrawl:
		pagina = get_html(tocrawl[0])
		if (pagina != ''):
			new_l = get_links(pagina)
			crawled.append(tocrawl[0])
			new_l = filter(lambda x: (x not in crawled and x not in tocrawl), new_l)
			tocrawl = tocrawl + new_l
		if tocrawl.pop(0) == last:
			last = tocrawl[-1]
			depth += 1
	return crawled


def easysearch():
	lis = []
	while True:
		word = raw_input()
		if word=='fin de la cita':
			return lis
		lis.append(word)


#print crawl_linear(['http://gonthalo.github.io', 'http://github.com/gonthalo'], 10)
#print crawl_linear(['http://www.google.es/'], 10)
elpais_urls = crawl_linear(['http://internacional.elpais.com/'], 20)
principal = get_html('http://internacional.elpais.com/')
tree = html.fromstring(principal)
nice_content = tree.xpath('//a[@title="Ver noticia"]')
print [link.get("href") for link in nice_content]
muchas_url = [link.get("href") for link in nice_content]
#print crawl_depth(['http://internacional.elpais.com/'], 1)
countries = ['Alemania', 'Espa&ntilde;a', 'Gran Breta&ntilde;a', 'Francia', 'Italia', 'Grecia', 'Catalu&ntilde;a', 'Portugal']
countries += ['Brasil', 'Argentina', 'Chile', 'Ecuador', 'Cuba', 'Venezuela', 'Estados Unidos', 'Mexico', 'Canad&aacute;']
countries += ['Rusia', 'India', 'Indonesia', 'China', 'Bangladesh', 'Jap&oacute;n', 'Iraq', 'Ir&aacute;n', 'Australia']
for country in countries:
	print country, '-'*(20 - len(country)), buscar(elpais_urls, [country]), buscar(muchas_url, [country])
