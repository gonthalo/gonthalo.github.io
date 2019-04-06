#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, inspect, sys, math
from datetime import datetime

ip = "0.0.0.0"

volver = False
try:
	import pygame, pygame.mixer
except:
	volver = True
	print "Missing library: Pygame"
from time import time
from random import random
from pygame.locals import *
try:
	from PIL import Image
except:
	volver = True
	print "Missing library: PIL (python image library)"

try:
	import socket
except:
	volver = True
	print "Missing library: socket"

try:
	import threading
except:
	volver = True
	print "Missing library: datetime"

try:
	os.system("unzip --help")
except:
	volver = True
	print "Missing 'unzip' utility. Try 'sudo apt install unzip'"

if volver:
	raw_input("Press ENTER to exit")
	sys.exit()

PATH = inspect.getfile(inspect.currentframe())[:-15]

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
FPS = 30
NEGRO = (0, 0, 0)
NABLA = (10, 200, 110)
BLANCO = (255, 255, 255)

PAD = 0

teclas = [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, 241,
K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_SPACE, K_COMMA, K_PERIOD, 45, 39, 231, 43, 60, 61]
LETRAS = u'!"·$%&/()=ABCDEFGHIJKLMNÑOPQRSTUVWXYZ ;:_?Ç*>¿'
letras = u"1234567890abcdefghijklmnñopqrstuvwxyz ,.-'ç+<¡"
diccio = {'hola': 'IDIOTA'}
for ii in range(len(teclas)):
	diccio[teclas[ii]] = LETRAS[ii]
	diccio[-teclas[ii]] = letras[ii]
acentuar = {'a':u'á', 'e':u'é', 'i':u'í', 'o':u'ó', 'u':u'ú', 'A':u'Á', 'E':u'É', 'I':u'Í', 'O':u'Ó', 'U':u'Ú'}


def wrr():
	return ['-', '/', '|', '\\'][int(time()*100)%4]

def n00():
	return

def ynt(num):
	if (num >= 0):
		return int(num)
	return int(num) - 1

class Imagen:
	def __init__(self, file_name):
		self.area = file_name
		self.rect = self.area.get_rect()
		self.x = self.rect.width
		self.y = self.rect.height
	def poner(self, i_x, i_y, phi=0):
		SCREEN.blit(pygame.transform.rotate(self.area, phi), self.rect.move(i_x, i_y))

def get_text(texto, fondo, frente, font, size):
	pygame.font.init()
	fuente = pygame.font.SysFont(font, size)
	if fondo == None:
		texto = fuente.render(texto, True, frente)
	else:
		texto = fuente.render(texto, True, frente, fondo)
	img_a = Imagen(pygame.image.fromstring('123', (1, 1), 'RGB'))
	img_a.area = texto
	img_a.rect = img_a.area.get_rect()
	img_a.x, img_a.y = img_a.rect.width, img_a.rect.height
	return img_a

class Texto:
	def __init__(self, posicion, cnt, fuente, fsize, color, colorf):
		self.posicion = posicion
		self.content = cnt
		self.rend = ''
		self.color = color
		self.colorf = colorf
		self.fuente = fuente
		self.fsize = fsize
		self.img = False
		self.rendx, self.rendy = self.posicion[0], self.posicion[1]
	def poner(self):
		if self.content != self.rend:
			self.rend = self.content
			self.img = get_text(self.rend, self.colorf, self.color, self.fuente, self.fsize)
			if self.posicion[0] == -1:
				self.rendx = SCREEN_WIDTH/2 - self.img.x/2
			if self.posicion[1] == -1:
				self.rendy = SCREEN_HEIGHT/2 - self.img.y/2
		self.img.poner(self.rendx, self.rendy)

def poner_texto(cadena, alto, fuen, tam, posi, color):
	pygame.font.init()
	fuente = pygame.font.SysFont(fuen, tam)
	dy = alto*len(cadena)/2
	for ind in range(len(cadena)):
		texto = fuente.render(cadena[ind], True, color, (0, 0, 0))
		dx = texto.get_rect().width/2
		SCREEN.blit(texto, texto.get_rect().move(posi[0] - dx, posi[1] + alto*ind - dy))

def giro(p, xx, yy, zz, cc, ss):
	res = [(cc + xx*xx*(1 - cc))*p[0] + (xx*yy*(1 - cc) - zz*ss)*p[1] + (xx*zz*(1 - cc) + yy*ss)*p[2]]
	res.append((xx*yy*(1 - cc) + zz*ss)*p[0] + (cc + yy*yy*(1 - cc))*p[1] + (yy*zz*(1 - cc) - xx*ss)*p[2])
	return res + [(xx*zz*(1 - cc) - yy*ss)*p[0] + (yy*zz*(1 - cc) + xx*ss)*p[1] + (cc + zz*zz*(1 - cc))*p[2]]

class Objeto:
	def __init__(self, puntos, lineas, caras, xxx, yyy):
		if xxx == -1:
			xxx = SCREEN_WIDTH/2
		if yyy == -1:
			yyy = SCREEN_HEIGHT/2
		self.puntos = puntos
		self.lineas = lineas
		self.caras = caras
		self.x, self.y = xxx, yyy
	def trasladar(self, vec):
		self.puntos = map(lambda x: [x[ii] + vec[ii] for ii in range(3)], self.puntos)
		#self.puntos = map(lambda x: [ynt(x[ii]*1000 + .5)*.001 for ii in range(3)], self.puntos)
	def girar(self, p0, p1, phi):
		self.trasladar([-el for el in p0])
		p1 = [p1[ii] - p0[ii] for ii in range(3)]
		nor = math.sqrt(sum(map(lambda x: x*x, p1)))
		xx, yy, zz = map(lambda x: x/nor, p1)
		cc = math.cos(phi)
		ss = math.sin(phi)
		self.puntos = map(lambda x: giro(x, xx, yy, zz, cc, ss), self.puntos)
		self.trasladar(p0)
	def escalar(self, k, ori = [0, 0, 0]):
		self.puntos = map(lambda x: [ori[ii] + k*(x[ii] - ori[ii]) for ii in range(3)], self.puntos)
	def dibujar(self, per = "ortogonal"):
		if per == "ortogonal":
			if self.lineas == []:
				for punto in self.puntos:
					pygame.draw.circle(SCREEN, (0, 0, 255), (ynt(punto[0] + .5) + self.x, ynt(punto[1] + .5) + self.y), 5)
			for linea in self.lineas:
				p1 = self.puntos[linea[0]]
				p2 = self.puntos[linea[1]]
				p1, p2 = map(lambda x: ynt(x + .5), p1), map(lambda x: ynt(x + .5), p2)
				pygame.draw.line(SCREEN, BLANCO, (p1[0] + self.x, p1[1] + self.y), (p2[0] + self.x, p2[1] + self.y), 3)
	def actualizar(self):
		self.girar([0, 0, 0], [1, 1, 1], 0.1)
		self.escalar(0.99 + 0.02*random())

exito = "Unknown"

def terminate():
	pygame.quit()
	if exito == "Correct":
		raw_input("PesterChum installation correct.\nPress ENTER to exit.")
	else:
		raw_input("PesterChum installation failed.\nReason: %s\nPress ENTER to exit."%exito)
	sys.exit()

class Pantalla:
	def __init__(self, escritores = [], listas = [], textos = [], objetos = []):
		self.elist = escritores
		self.tlist = textos
		self.llist = listas
		self.olist = objetos
		self.shift_pressed = False
		self.selected = -1
		self.del_pressed = False
		self.del_lag = False
	def poner(self):
		SCREEN.fill(NEGRO)
		for texto in self.tlist:
			texto.poner()
		for ind in range(len(self.elist)):
			ven = self.elist[ind]
			ven.poner(writing = (ind==self.selected))
		for lista in self.llist:
			lista.poner()
		for obj in self.olist:
			obj.dibujar()
		pygame.display.update()
	def actualizar(self, mousex, mousey, clic):
		for obj in self.olist:
			obj.actualizar()
		for ind in range(len(self.elist)):
			ven = self.elist[ind]
			if clic and (mousex > ven.posicion[0] - ESQ/2 and mousey > ven.posicion[1] - ESQ/2 and mousex - ven.posicion[0] < ven.size[0] + ESQ/2 and mousey - ven.posicion[1] < ven.size[1] + ESQ/2):
				self.selected = ind
		if self.selected != -1 and self.del_pressed and self.del_lag<time():
			self.elist[self.selected].escribir(8, False)
	def pulsar(self, tec):
		if tec == K_RSHIFT or tec == K_LSHIFT:
			self.shift_pressed = True
			return
		if tec == 8:
			self.del_pressed = True
			self.del_lag = time()+0.15
		if tec == 27:#Escape
			self.selected = -1
		if self.selected != -1:
			if tec == 9:
				self.selected = (self.selected + 1)%len(self.elist)
			self.elist[self.selected].escribir(tec, self.shift_pressed)
	def soltar(self, tec):
		if tec == K_RSHIFT or tec == K_LSHIFT:
			self.shift_pressed = False
		if tec == 8:
			self.del_pressed = False

#Funciones locales

def recibir_arch(a):
	a.send("START")
	size = int(a.recv(1024))
	a.send("OK;")
	c = 0.
	texto = ''
	while c<size:
		inf = a.recv(1024)
		texto = texto + inf
		c += 1024
		print "Recibido %.1f%s"%(100.*c/size, "%")
		a.send("OK;")
	print "Recibido 100%"
	return texto

def instalar():
	global exito
	try:
		port = 12357
		c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		c.connect((ip, port))
	except:
		exito = "Server down"
		return
	c.send("Los japoneses:\n")
	c.recv(1024)
	c.send("son imbeciles.\n")
	c.recv(1024)
	c.send("USER SendMe")
	c.recv(1024)
	c.send("PASS TheClient")
	version = c.recv(1024)
	texto = recibir_arch(c)
	c.close()
	name = "PC-%s.zip"%version
	arch = open(name, "w")
	arch.write(texto)
	arch.close()
	os.system("mkdir ~/PesterChum")
	os.system("unzip %s -d ~/PesterChum"%name)
	os.system("rm %s"%name)
	exito = "Correct"

#Funciones principales

def main():
	global FPSCLOCK, SCREEN
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	#pygame.display.set_icon([...])
	SCREEN = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption('PesterChum Installer')
	runGame()

def runGame():
	def nada():
		return
	myobj = Objeto([[0, 0, 0], [100, 0, 0], [100, 100, 0], [100, 0, 100], [100, 100, 100], [0, 0, 100], [0, 100, 0], [0, 100, 100]],
	[[0, 1], [1, 2], [0, 5], [0, 6], [1, 3], [4, 2], [4, 7], [4, 3], [5, 7], [2, 6], [3, 5], [6, 7]], [], 200, 200)
	myobj.trasladar([-50, -50, -50])
	myobj.girar([0, 0, 0], [3, -7, 1], 2*math.pi/3.)
	myobj.girar([2, 2, 2], [1, -1, 1], 4*math.pi/3.)
	TEXTOS = [Texto([-1, 40], 'Installing...', "tlwgtypewriter", 40, BLANCO, False)]
	mipan = Pantalla(textos = TEXTOS, objetos = [myobj])
	mousex, mousey = 0, 0
	mouseclic = False
	t = threading.Thread(target = instalar)
	t.start()
	while True:
		FPSCLOCK.tick(FPS)
		mouseclic = False
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYUP:
				mipan.soltar(event.key)
			elif event.type == KEYDOWN:
				mipan.pulsar(event.key)
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseclic = True
		mipan.poner()
		mipan.actualizar(mousex, mousey, mouseclic)
		if not t.isAlive():
			terminate()

if __name__ == "__main__":
	main()

