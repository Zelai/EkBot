#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys
import interface
import copy # para copiar listas

class ZelaiBot(interface.Bot):
	"""Bot ZelaiBot 0.1"""
	NAME = "ZelaiBot 0.1"""

	def __init__(self, init_state):
		"""Inicializar el bot: llamado al comienzo del juego."""
		# llamada a super para inicializar las variables (self.)
		#  player_num, player_count, position, map, lighthouses
		interface.Bot.__init__(self,init_state)	

	def play(self, state):
		"""Jugar: llamado cada turno.
		Debe dev olver una accion (jugada)."""
		self.log("hola " + str(self.player_num)) 
		return self.move(*(-1,0))	

if __name__ == "__main__":
	iface = interface.Interface(ZelaiBot)
	iface.run()
