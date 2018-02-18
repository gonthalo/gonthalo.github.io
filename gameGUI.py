#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, inspect, sys, math, random, pygame, pygame.mixer
from time import time
from random import random
from pygame.locals import *
from PIL import Image
from datetime import datetime

PATH = inspect.getfile(inspect.currentframe())[:-12]

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FPS = 30
NEGRO = (0, 0, 0)
NABLA = (10, 200, 110)
BLANCO = (255, 255, 255)

if True == True:
	img_aux = Image.new('RGB', (1, 1), 'black')
	img_aux.save(PATH + 'img/void.png')

img_esquina = Image.open(PATH + 'img/esquina.png')
MAT_ESQ = [[1.-img_esquina.getpixel((ii, jj))[0]/255. for jj in range(img_esquina.size[1])] for ii in range(img_esquina.size[0])]
ESQ = 22
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

class Imagen:
	def __init__(self, file_name):
		self.area = pygame.image.load(PATH + 'img/' + file_name)
		self.rect = self.area.get_rect()
		self.x = self.rect.width
		self.y = self.rect.height
	def poner(self, i_x, i_y, phi=0):
		SCREEN.blit(pygame.transform.rotate(self.area, phi), self.rect.move(i_x, i_y))

class Boton:
	def __init__(self, xxx, yyy, texto, accion):
		self.texto = texto
		self.accion = accion
		if xxx == -1:
			xxx = SCREEN_WIDTH/2 - self.texto.x/2
		if yyy == -1:
			yyy = SCREEN_HEIGHT/2 - self.texto.y/2
		posicion = self.x, self.y = xxx, yyy
		size = (texto.x, texto.y)
		img_aux = Image.new('RGB', (size[0] + 2*ESQ + 2*PAD, size[1] + 2*ESQ + 2*PAD), 'black')
		for jj in range(-1, 1):
			for ii in range(size[0] + 2*PAD):
				img_aux.putpixel((ii + ESQ, jj + ESQ/2), NABLA)
				img_aux.putpixel((ii + ESQ, size[1] + 2*PAD + 3*ESQ/2 - 1 - jj), NABLA)
			for ii in range(size[1] + 2*PAD):
				img_aux.putpixel((jj + ESQ/2, ii + ESQ), NABLA)
				img_aux.putpixel((size[0] + 2*PAD + 3*ESQ/2 - 1 - jj, ii + ESQ), NABLA)
		for vx, vy, matriz in [(0, 0, MAT_ESQ),
		(size[0] + 2*PAD + ESQ, 0, [[MAT_ESQ[jj][ESQ - 1 - ii] for jj in range(ESQ)] for ii in range(ESQ)]),
		(size[0] + 2*PAD + ESQ, size[1] + 2*PAD + ESQ, [[MAT_ESQ[ESQ - 1 - ii][ESQ - 1 - jj] for jj in range(ESQ)] for ii in range(ESQ)]),
		(0, size[1] + 2*PAD + ESQ, [[MAT_ESQ[ESQ - 1 - jj][ii] for jj in range(ESQ)] for ii in range(ESQ)])]:
			for ii in range(ESQ):
				for jj in range(ESQ):
					img_aux.putpixel((ii + vx, jj + vy), tuple([int(tt*matriz[ii][jj]) for tt in (10, 200, 110)]))
		path_aux = 'b_image_' + str(posicion[0]) + '_' + str(posicion[1]) + '.png'
		img_aux.save(PATH + 'img/' + path_aux)
		self.fondo = Imagen(path_aux)
	def dibujar(self):
		self.fondo.poner(self.x - ESQ - PAD, self.y - ESQ - PAD)
		self.texto.poner(self.x, self.y)
	def clicar(self, mousex, mousey):
		if (mousex > self.x - ESQ/2 and mousey > self.y - ESQ/2 and mousex - self.x < self.texto.x + ESQ/2 and mousey - self.y < self.texto.y + ESQ/2):
			self.accion()

def get_text(texto, fondo, frente, font, size):
	pygame.font.init()
	fuente = pygame.font.SysFont(font, size)
	if fondo == None:
		texto = fuente.render(texto, True, frente)
	else:
		texto = fuente.render(texto, True, frente, fondo)
	img_a = Imagen('void.png')
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

class Escritor:
	def __init__(self, posicion, size, cnt, fsize = 20, fcolor = NABLA):
		img_aux = Image.new('RGB', (size[0] + 2*ESQ + 2*PAD, size[1] + 2*ESQ + 2*PAD), 'black')
		for jj in range(-1, 1):
			for ii in range(size[0] + 2*PAD):
				img_aux.putpixel((ii + ESQ, jj + ESQ/2), fcolor)
				img_aux.putpixel((ii + ESQ, size[1] + 2*PAD + 3*ESQ/2 - 1 - jj), fcolor)
			for ii in range(size[1] + 2*PAD):
				img_aux.putpixel((jj + ESQ/2, ii + ESQ), fcolor)
				img_aux.putpixel((size[0] + 2*PAD + 3*ESQ/2 - 1 - jj, ii + ESQ), fcolor)
		for vx, vy, matriz in [(0, 0, MAT_ESQ),
		(size[0] + 2*PAD + ESQ, 0, [[MAT_ESQ[jj][ESQ - 1 - ii] for jj in range(ESQ)] for ii in range(ESQ)]),
		(size[0] + 2*PAD + ESQ, size[1] + 2*PAD + ESQ, [[MAT_ESQ[ESQ - 1 - ii][ESQ - 1 - jj] for jj in range(ESQ)] for ii in range(ESQ)]),
		(0, size[1] + 2*PAD + ESQ, [[MAT_ESQ[ESQ - 1 - jj][ii] for jj in range(ESQ)] for ii in range(ESQ)])]:
			for ii in range(ESQ):
				for jj in range(ESQ):
					img_aux.putpixel((ii + vx, jj + vy), tuple([int(tt*matriz[ii][jj]) for tt in fcolor[:3]]))
		path_aux = 'e_image_' + str(posicion[0]) + '_' + str(posicion[1]) + '.png'
		img_aux.save(PATH + 'img/' + path_aux)
		self.fondo = Imagen(path_aux)
		self.posicion = posicion
		self.size = size
		self.content = cnt
		self.fuente = 'courier'
		self.fsize = fsize
		self.fcolor = fcolor
	def poner(self, writing = False):
		chain = []
		elem = ''
		for item in (self.content + writing*wrr()).split(' '):
			if (len(elem) + len(item))*self.fsize/1.5 > self.size[0] + ESQ - 6:
				chain.append(elem)
				elem = item
				continue
			elem = elem  + ' '*(elem != '') + item
		chain.append(elem)
		self.fondo.poner(self.posicion[0]-ESQ, self.posicion[1]-ESQ)
		poner_texto(chain, self.fsize, self.fuente, self.fsize, (self.posicion[0] + self.size[0]/2, self.posicion[1] + self.size[1]/2), self.fcolor)
		return
		img_aux = get_text(self.content, False, self.fcolor, self.fuente, self.fsize)
		img_aux.poner(posicion)
	def escribir(self, tecla, shift, borrar = False):
		if tecla == 8 or borrar:
			self.content = self.content[:-1]
		if tecla in teclas:
			if shift:
				self.content += diccio[tecla]
			else:
				self.content += diccio[-tecla]
			if len(self.content)>1 and self.content[-2]==u'ç' and self.content[-1] in 'AEIUOeaiuo':
				self.content = self.content[:-2] + acentuar[self.content[-1]]
		elif tecla != 8:
			print tecla
		if tecla == K_KP_ENTER:
			self.content += ':('

class Lista:
	def __init__(self, posicion, size, cnt, fsize = 20, fcolor = NABLA, actions = []):
		n = len(cnt)
		img_aux = Image.new('RGB', (size[0] + 2*ESQ + 2*PAD, size[1] + 2*ESQ + 2*PAD), 'black')
		for jj in range(-1, 1):
			for ii in range(size[0] + 2*PAD):
				img_aux.putpixel((ii + ESQ, jj + ESQ/2), fcolor)
				img_aux.putpixel((ii + ESQ, size[1] + 2*PAD + 3*ESQ/2 - 1 - jj), fcolor)
			for ii in range(size[1] + 2*PAD):
				img_aux.putpixel((jj + ESQ/2, ii + ESQ), fcolor)
				img_aux.putpixel((size[0] + 2*PAD + 3*ESQ/2 - 1 - jj, ii + ESQ), fcolor)
		for vx, vy, matriz in [(0, 0, MAT_ESQ),
		(size[0] + 2*PAD + ESQ, 0, [[MAT_ESQ[jj][ESQ - 1 - ii] for jj in range(ESQ)] for ii in range(ESQ)]),
		(size[0] + 2*PAD + ESQ, size[1] + 2*PAD + ESQ, [[MAT_ESQ[ESQ - 1 - ii][ESQ - 1 - jj] for jj in range(ESQ)] for ii in range(ESQ)]),
		(0, size[1] + 2*PAD + ESQ, [[MAT_ESQ[ESQ - 1 - jj][ii] for jj in range(ESQ)] for ii in range(ESQ)])]:
			for ii in range(ESQ):
				for jj in range(ESQ):
					img_aux.putpixel((ii + vx, jj + vy), tuple([int(tt*matriz[ii][jj]) for tt in fcolor[:3]]))
		for jj in range(1, n):
			for ii in range(size[0]+ESQ):
				img_aux.putpixel((ii + ESQ/2, ESQ/2+int((size[1]+ESQ)*jj/n)), fcolor)
		path_aux = 'l_image_' + str(posicion[0]) + '_' + str(posicion[1]) + '.png'
		img_aux.save(PATH + 'img/' + path_aux)
		self.fondo = Imagen(path_aux)
		self.posicion = posicion
		self.size = size
		self.content = cnt
		self.fuente = 'courier'
		self.fsize = fsize
		self.fcolor = fcolor
		self.centers = [self.posicion[1]-ESQ/2 + int(0.5+(2*ii+1.)*(self.size[1]+ESQ)/(2.*n)) for ii in range(n)]
		self.acts = [n00 for ii in range(n)]
		if actions:
			self.acts = actions
	def poner(self, writing = False):
		self.fondo.poner(self.posicion[0]-ESQ, self.posicion[1]-ESQ)
		n = len(self.content)
		for ii in range(n):
			chain = []
			elem = ''
			for item in (self.content[ii] + writing*wrr()).split(' '):
				if (len(elem) + len(item))*self.fsize/1.5 > self.size[0] + ESQ - 6:
					chain.append(elem)
					elem = item
					continue
				elem = elem  + ' '*(elem != '') + item
			chain.append(elem)
			poner_texto(chain, self.fsize, self.fuente, self.fsize, (self.posicion[0] + self.size[0]/2, self.centers[ii]), self.fcolor)
	def clicar(self, mousex, mousey):
		if (mousex > self.posicion[0] - ESQ/2 and mousey > self.posicion[1] - ESQ/2
		 and mousex - self.posicion[0] < self.size[0] + ESQ/2 and mousey - self.posicion[1] < self.size[1] + ESQ/2):
			n = len(self.content)
			num = int(n*(mousey-self.posicion[1] + ESQ/2)/(self.size[1]+ESQ))
			self.acts[num]()


def spam_imgs(lis):
	for text, xx, yy in lis:
		if xx == -1:
			xx = SCREEN_WIDTH/2 - text.rect[2]/2
		if yy == -1:
			yy = SCREEN_HEIGHT/2 - text.rect[3]/2
		text.poner(xx, yy)

def terminate():
	pygame.quit()
	sys.exit()

class Pantalla:
	def __init__(self, botones = [], escritores = [], imagenes = [], listas = [], textos = []):
		self.elist = escritores
		self.ilist = imagenes
		self.blist = botones
		self.tlist = textos
		self.llist = listas
		self.shift_pressed = False
		self.selected = -1
		self.del_pressed = False
		self.del_lag = False
	def poner(self):
		SCREEN.fill(NEGRO)
		spam_imgs(self.ilist)
		for boton in self.blist:
			boton.dibujar()
		for texto in self.tlist:
			texto.poner()
		for ind in range(len(self.elist)):
			ven = self.elist[ind]
			ven.poner(writing = (ind==self.selected))
		for lista in self.llist:
			lista.poner()
		pygame.display.update()
	def actualizar(self, mousex, mousey, clic):
		if clic:
			for boton in self.blist:
				boton.clicar(mousex, mousey)
			for lis in self.llist:
				lis.clicar(mousex, mousey)
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


#Funciones principales

def main():
	global FPSCLOCK, SCREEN
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	#pygame.display.set_icon([...])
	SCREEN = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption('Nombre de la ventana')
	runGame()


def runGame():
	def nada():
		TEXTOS[0].content += 'a'
	def imagine():
		IMAGENES[0] = (Imagen("canvas.png"), 100, 300)
	VENTANAS = [Escritor((100, 100), (200, 50), u'Escribe aquí')]
	LISTADO = [Lista((800, 200), (200, 200), [u'Muy buenos días', 'Esto es una lista', 'Supongamos que funciona', u'Pinche aquí'], actions = [n00, n00, n00, imagine])]
	BOTONES = [Boton(-1, 440, get_text(u'Botón', False, NABLA, 'Arial', 20), nada)]
	IMAGENES = [(Imagen("void.png"), 0, 0)]
	TEXTOS = [Texto([-1, 40], 'Texto de prueba', "tlwgtypewriter", 40, BLANCO, False)]
	mipan = Pantalla(botones = BOTONES, escritores = VENTANAS, imagenes = IMAGENES, textos = TEXTOS, listas = LISTADO)
	mousex, mousey = 0, 0
	mouseclic = False
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


main()
