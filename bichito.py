#comments comments comments
###comments R FAN
"""although I don't Us dem cose aim sach ah bud person"""
import urllib, urllib2
from lxml import html

def get_html(some_url):
	page = 'nadademomento'
	try:
		page = urllib2.urlopen(some_url)
	except urllib2.HTTPError, e:
		print e.fp.read()
		return 'muymal'
	except:
		print 'Los rusos han tratado de detener al crawler. Muy pero que muy mal.'
		return 'muymal'
	return page.read()

def get_next_link(page):
	v1 = page.find('<a href=')
	if v1 == -1:
		return False, 0
	print v1, page[v1:v1 + 25]
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

def crawl_linear(links, maxi):
	tocrawl = copy(links)
	count = 0
	crawled = []
	while count < maxi and tocrawl:
		new_l = get_links(get_html(tocrawl[0]))
		crawled.append(tocrawl.pop(0))
		new_l = filter(lambda x: (x not in crawled and x not in tocrawl), new_l)
		tocrawl = tocrawl + new_l
		count += 1
	return crawled


def crawl_depth(links, max_depth):
	tocrawl = copy(links)
	depth = 0
	crawled = []
	last = tocrawl[-1]
	while depth < max_depth and tocrawl:
		new_l = get_links(get_html(tocrawl[0]))
		crawled.append(tocrawl[0])
		new_l = filter(lambda x: (x not in crawled and x not in tocrawl), new_l)
		tocrawl = tocrawl + new_l
		if links.pop(0) == last:
			last = tocrawl[0]
			depth += 1
	return crawled

print crawl_linear(['http://gonthalo.github.io', 'http://github.com/gonthalo'], 100)
print crawl_linear(['http://www.google.es/'], 100)
