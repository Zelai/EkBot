#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys
import interface
import copy # para copiar listas

class ZelaiBot(interface.Bot):
	"""Bot ZelaiBot 0.1"""
	NAME = "ZelaiBot 0.1"""


	distancias = {}

	def __init__(self, init_state):
		"""Inicializar el bot: llamado al comienzo del juego."""
		# llamada a super para inicializar las variables (self.)
		#  player_num, player_count, position, map, lighthouses
		interface.Bot.__init__(self,init_state)	

		# La distancia Maxima es la máxima entre el número de casillas
		# en x y el número de casillas en y (se puede mover en diagonal)
		self.xMax = len(self.map[1]);
		self.yMax = len(self.map);
		distanciaMax = max(self.xMax,self.yMax) + 1
	
		self.mapa = str(self.map)
		self.log(self.mapa)
		mapaAux = self.map[:]	
		
		self.log("lighthouses:\n" + str(self.lighthouses));
		self.log("len(lighthouses)=%d\n" %  (len(self.lighthouses)) );
		
		self.log("xMax=" + str(self.xMax) + " yMax="+ str(self.yMax) + "\n")
		# posiciones validas map[0][0] - map[17,20]
		# modo de acceso map[y][x]

		for faro in range(len(self.lighthouses)):
			self.distancias[faro] = copy.deepcopy(self.map[:])	
		self.log("len(lighthouses)="+ str(len(self.lighthouses)) + "\n" +str(self.distancias[0]))
		### Pendiente: convertir el mapa de 0 y 1 a -1 y distanciaMax
#		[self.distancias[faro][y][x] = 

	def play(self, state):
		"""Jugar: llamado cada turno.
		Debe dev olver una accion (jugada)."""
		self.log("hola " + str(self.player_num)) 
		return self.move(*(-1,0))	

if __name__ == "__main__":
	iface = interface.Interface(ZelaiBot)
	iface.run()
