#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys
import interface
import copy # para copiar listas


distancias = {}
estado = {}

def muestra(variable, nombre):
	sys.stderr.write('\n---- inicio muestra----\n')
	auxTipo = type(variable)

	# Para imprimir una lista:
	if auxTipo.__name__ == 'list':
		sys.stderr.write("variable: " + nombre + "   tipo: " + auxTipo.__name__ + "\n")
		for i in xrange(len(variable)):
			texto = "%02d" % i
			sys.stderr.write("[" + texto + "]=")
			for j in xrange(len(variable[i])):
				texto = "%1d " % variable[i][j]
				sys.stderr.write(texto )
			sys.stderr.write("\n")
	sys.stderr.write("\n")

	# Para imprimir un diccionario:
	if auxTipo.__name__ == 'dict':
		sys.stderr.write("variable: " + nombre + "   tipo: " + auxTipo.__name__ + "\n")
		texto = str(variable)
		sys.stderr.write(texto + "\n")
	if auxTipo.__name__ == 'int':
		sys.stderr.write("variable: " + nombre + "  tipo: " + auxTipo.__name__ + " valor: " + str(variable) +"\n")

	sys.stderr.write('---- fin muestra----\n\n')

def distanciasRec(faro,punto, dist):
	debug = 0 
	if debug >0: sys.stderr.write("Entro en distanciasRec("+ str(faro) +"," + "[" + str(punto[0]) + "," + str(punto[1]) + "],"+str(dist)+ ")\n")
	if debug >1: sys.stderr.write("   punto tipo " + type(punto).__name__ + " punto=(" + str(punto[0]) + "," + str(punto[1]) +")\n")		
	mapa=distancias[faro]
	if debug >2: muestra(mapa,'mapa')
	if debug > 2: sys.stderr.write("len(punto)=" + str(len(punto)))
	if debug > 2: sys.stderr.write(" punto[0]=" + str(punto[0]))
	if debug > 2: sys.stderr.write(" punto[1]=" + str(punto[1])+ "\n")
	a=punto[0]
	b=punto[1]
	longX = len(mapa)
	longY = len(mapa[0])
	if mapa[punto[0]][punto[1]] > dist:
		mapa[punto[0]][punto[1]] = dist
		if a > 0: distanciasRec(faro,[a-1,b],dist + 1)
		if a < longX: distanciasRec(faro,[a+1,b], dist+1)
		if b > 0: distanciasRec(faro,[a,b-1],dist + 1)
		if b < longY: distanciasRec(faro,[a,b+1], dist +1)
		if a > 0 and b > 0: distanciasRec(faro,[a-1,b-1], dist +1)
		if a > 0 and b < longY: distanciasRec(faro,[a-1,b+1], dist +1)
		if a < longX and b > 0: distanciasRec(faro,[a+1,b-1], dist +1)
		if a < longX and b < longY: distanciasRec(faro,[a+1,b+1], dist +1)
		
	else:
		return
	if debug >0: sys.stderr.write("Salgo de distanciasRec\n")
	return 

def calculaDistancias(lighthouses, mapa):
	debug = 0
	if debug > 0: sys.stderr.write("Entro en calculaDistancias\n")
	if debug > 1: sys.stderr.write("longX="+ str(len(mapa)) + " longY=" +str(len(mapa[1])) + "\n")
	n_lighthouses = len(lighthouses)
	if debug > 2: sys.stderr.write("nº lighthouses = " + str(n_lighthouses) + "\n")
	mapaAux= mapa[:]
	if debug > 2:muestra(mapaAux, 'mapaAux')
	mapaAux = [[1000 * i for i in x ] for x in mapaAux]	

	for faro in range(len(lighthouses)):
		mapaAuxFaro = copy.deepcopy(mapaAux[:])
		distancias[faro]=mapaAuxFaro[:]
		distanciasRec(faro,lighthouses[faro], 1)

	if debug > 0: sys.stderr.write("Salgo de calculaDistancias\n")
	return  

class ZelaiBot(interface.Bot):
    """Bot Zelai 0.1"""
    NAME = "ZelaiBot 0.1"

    def __init__(self, init_state):
        """Inicializar el bot: llamado al comienzo del juego."""
	debug = 0
	if debug > 0: sys.stderr.write("Entro en __ini__\n")
        self.player_num = init_state["player_num"]
        self.player_count = init_state["player_count"]
        self.init_pos = init_state["position"]
        self.map = init_state["map"]
        self.lighthouses = map(tuple, init_state["lighthouses"])
	self.inicializa()
	if debug > 1: muestra(distancias[0],'distancias[0]')
	if debug > 1: muestra(distancias[1],'distancias[1]')
	if debug > 0: sys.stderr.write("Salgo de __ini__\n")

    def inicializa(self):
	debug = 0
	if debug > 0: sys.stderr.write("""
		------- Inicio inicializa-------
		""")
	if debug > 1:muestra(self.lighthouses,"self.ligthouses")
	if debug > 1:muestra(self.map,"self.map")
	if debug > 1:sys.stderr.write("longitud x:" + str(len(self.map)) + " y:" + str(len(self.map[0])) + "\n")
	longX = len(self.map)
	longY = len(self.map[0])
	if debug > 1:sys.stderr.write("numero lighouses = " + str(len(self.lighthouses)) + "\n")
	
	calculaDistancias(self.lighthouses, self.map)
	estado['accion']=0
	estado['destino']=0
	if debug > 1:sys.stderr.write("""
		------- fin inicializa-------
		""")
    def buscaFaro(self,x,y,lighthouses):
	debug = 3
	if debug >0: sys.stderr.write("Entro en buscaFaro\n")

	#estado['accion'] = 1 
	faroMin=0
	distanciaMin = distancias[0][x][y]
	
	if distanciaMin == 1 and estado["accion"] != 2: distanciaMin = 100

	if debug > 2: sys.stderr.write("Posicion actual:(" + str(x) + "," + str(y) + ")\n")
	for faro in range(len(lighthouses)):
		#if distancias[faro][x][y] < distanciaMin:
		if debug > 2: sys.stderr.write(" bucle faro %d distancia = %d distanciaMin = %d\n" % (faro,distancias[faro][x][y],distanciaMin))
		if distancias[faro][x][y] < distanciaMin and estado["accion"] != 2:
#			faroMin = faro
#			distanciaMin = distancias[faro][x][y]
#			muestra(lighthouses,'lighthouses')
			if (x,y) in lighthouses:
				if debug > 2: sys.stderr.write("  (x,y) in lighthouses\n");
				if lighthouses[(x,y)]["owner"] == self.player_num:
					if debug > 2: sys.stderr.write("  owner coincide\n");
					continue
			
			if debug > 2: sys.stderr.write(" faromin=%d distanciaMin=%d\n" % (faro,distancias[faro][x][y]));
			faroMin = faro
			distanciaMin = distancias[faro][x][y]
#				if debug > 2: 
#					sys.stderr.write(" faro[" + str(faro) + "]=("+ str(lighthouses[faro][0]) + "," + str(lighthouses[faro][1]) + ")  distancia = " + str(distancias[faro][x][y]) + "\n")
#					sys.stderr.write("  faroMin = %d\n" % faroMin)
	estado['destino'] = faroMin	
	estado['accion'] = 1		
	if debug > 0: sys.stderr.write("Salgo de buscaFaro\n")
	return


    def reduce(self,x,y):
	debug = 1
	if debug > 0: sys.stderr.write("Entro en reduce, destino = %d distancia=%d\n" % (estado['destino'], distancias[estado['destino']][x][y]))

	faroDestino = estado['destino']
	distancia = distancias[faroDestino]

	xDest = 0
	yDest = 0
	distanciaMin = distancia[x][y]
	
	for xAux in [-1,0,1]:
		for yAux in [-1,0,1]:
			if self.map[x+xAux][y+yAux]:
				if distancia[x+xAux][y+yAux] < distanciaMin and distancia[x+xAux][y+yAux] != 0:
					distanciaMin =	distancia[x+xAux][y+yAux] 
					xDest = xAux
					yDest = yAux
					if debug > 2: sys.stderr.write("xDest=%d yDest=%d  xAux=%d yAux=%d, distanciaMin=%d\n" % (xDest,yDest,xAux,yAux,distanciaMin))

	# Si voy a llegar a un faro
	if distanciaMin ==1:
		estado['accion']=2

	if debug > 1: sys.stderr.write("distanciaMin = %d\n" % distanciaMin)

	
	if debug > 0: sys.stderr.write("Salgo de reduce\n")
	return self.move(*(xDest,yDest))

    def faroMio(self,x,y,lighthouses):
	debug = 0
	esMio = False
	if debug > 0: sys.stderr.write("Entro en faroMio x=%d, y=%d energia=%d\n" % (x,y,self.energia))
	if lighthouses[(x,y)]["owner"] == self.player_num:
		esMio = True
	if debug > 2: muestra(lighthouses,'lighthouses')
	if debug > 0: sys.stderr.write("Salgo de faroMio esMio=%r\n"%(esMio))
	return esMio

    def play(self, state):
        """Jugar: llamado cada turno.
        Debe devolver una acción (jugada)."""
	debug=2
	if debug >0: sys.stderr.write("Entro en play, accion=%d, destino=%d\n" % (estado["accion"], estado["destino"]))

        cx, cy = state["position"]
        lighthouses = dict((tuple(lh["position"]), lh)
                            for lh in state["lighthouses"])
	self.energia= state["energy"]
	#sys.stderr.write("Map=" +  type(self.map).__name__ + "\n")

        if (cx, cy) in self.lighthouses:
            # Probabilidad 60%: conectar con faro remoto válido
            if lighthouses[(cx, cy)]["owner"] == self.player_num:
	    	possible_connections = []
                for dest in self.lighthouses:
                        # No conectar con sigo mismo
                        # No conectar si no tenemos la clave
                        # No conectar si ya existe la conexión
                        # No conectar si no controlamos el destino
                        # Nota: no comprobamos si la conexión se cruza.
                       if (dest != (cx, cy) and
                           lighthouses[dest]["have_key"] and
                           [cx, cy] not in lighthouses[dest]["connections"] and
                           lighthouses[dest]["owner"] == self.player_num):
                           possible_connections.append(dest)

		if possible_connections:
			if debug >0: sys.stderr.write("Salgo de play, accion=%d, conecto\n" % (estado["accion"]))
			return self.connect(random.choice(possible_connections))
		###if random.randrange(100) < 60:
		if self.energia > 10:
			#energy = random.randrange(state["energy"] + 1)
			energy = self.energia
			if debug >0: sys.stderr.write("Salgo de play, accion=%d, ataco\n" % (estado["accion"]))
			return self.attack(energy)

	hacer = []
       # Si estamos en un faro...
	if estado['accion'] == 0: # No hay accion definida
		self.buscaFaro(cx,cy,lighthouses)
	if estado['accion'] == 1: # Buscando un faro
		if debug >0: sys.stderr.write("Salgo de play, accion=%d, reduce\n" % (estado["accion"]))
		return self.reduce(cx,cy)
	if estado['accion'] == 2: #
		if debug > 1: sys.stderr.write("Estado=%d, faroMio=%r\n" % (estado['accion'], self.faroMio(cx,cy,lighthouses)))
		if not self.faroMio(cx,cy,lighthouses):
			if self.energia > lighthouses[(cx,cy)]["energy"] +1:
				estado['accion']=0
				#estado['destino']= (estado['destino'] + 1) % len(lighthouses)
				if debug >0: sys.stderr.write("Salgo de play, accion=%d, ataco\n" % (estado["accion"]))
				return self.attack(self.energia)
			
		estado['accion']=1
		#estado['destino']=random.randrange(len(lighthouses))
		if debug >0: sys.stderr.write("Salgo de play, accion=%d, reduce\n" % (estado["accion"]))
		return self.reduce(cx,cy)
	#return hacer
           # Probabilidad 60%: recargar el faro
       # Mover aleatoriamente
        moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        # Determinar movimientos válidos
        moves = [(x,y) for x,y in moves if self.map[cy+y][cx+x]]
        move = random.choice(moves)
	if debug >0: sys.stderr.write("Salgo de play\n")
	if debug >0: sys.stderr.write("Salgo de play, accion=%d, muevo aleatorio\n" % (estado["accion"]))
        return self.move(*move)

if __name__ == "__main__":
    iface = interface.Interface(ZelaiBot)
    iface.run()
