#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys
import interface
import copy # para copiar listas

class ZelaiBot(interface.Bot):
	"""Bot ZelaiBot 0.1"""
	NAME = "ZelaiBot 0.1"""

	def play(self, state):
		"""Jugar: llamado cada turno.
		Debe dev olver una accion (jugada)."""
		return self.move(*(-1,0))	
if __name__ == "__main__":
	iface = interface.Interface(ZelaiBot)
	iface.run()
