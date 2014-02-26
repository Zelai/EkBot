#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys
import interface
import copy # para copiar listas
import itertools


def logFun(ident, message, *args):
    """Mostrar mensaje de registro por stderr"""
    print >>sys.stderr, "[%s] %s" % (ident, (message % args))
       
class ZelaiBot(interface.Bot):
    """
    .. module::ZelaiBot
    """
    """Bot ZelaiBot 0.1"""
    NAME = "ZelaiBot 0.1"""

    def __init__(self, init_state):
        """Inicializar el bot: llamado al comienzo del juego.

|        Llama al init de interface para actualizar algunas variables
|            self.player_num
|            self.player_count
|            self.init_pos
|            self.map
|            self.lighthouses
|        Llama a calcular las distancias
|            self.distancias [faro][y][x]
|               una matriz por cada faro con su distancia al punto [y][x].

        :meth: interface.Bot.__init__
        """
        d=0
        if d>0: self.log("Entro en __init__")

        # llamada a super para inicializar las variables (self.)
        #  player_num, player_count, position, map, lighthouses
 
        interface.Bot.__init__(self,init_state) 

        if d>1: self.log(str(self.map))
        if d>1: self.log("lighthouses:\n" + str(self.lighthouses));
        
        # posiciones validas map[0][0] - map[17,20]
        # modo de acceso map[y][x]
        self.distancias = self.calculaDistancias(self.lighthouses,self.map) 
        
        self.estado = 0
        self.destino = 0
        
        if d>0: self.log("Salgo de__init__")

    def logeaFaro(self,faro):
        """ Esta función muestra el estado de un faro """
        self.log(("faro=%2d %8s  owner %4s   energy %4d   have_key %5s    connections:%s") % (
                faro,
                str(self.lighthouses.values()[faro]['position']),
                self.state['lighthouses'][faro]["owner"],
                self.state['lighthouses'][faro]["energy"],
                str(self.state['lighthouses'][faro]["have_key"]),
                str(self.state['lighthouses'][faro]["connections"])))

    def logeaFaros(self):
        """ Esta función muestra el estado de todos los faros """
        for faro in range(len(self.lighthouses)):
            self.logeaFaro(faro)
            
    def logeaEstado(self):
        """ Esta función muestra el estado """
        self.log(" XXX" + str(self.state) + "XXX")
        self.log(("Estado: posicion %8s  energia %4d   puntos %8d vista:") %(
            self.state['position'],
            self.state['energy'],
            self.state['score']))
        for i in range(5):
            cadena=[ "%4d" % pos for pos in self.state['view'][i]]
            self.log("     [" + str(cadena) + "]")
            

    def calculaDistancia(self, faro,mapa):
        """
        Esta función devuelve las distancias de un mapa
        a uno de los faros.


        :param tuple faro: tupla que contiene la posición del faro (x,y)
        :param list mapa: Lista 2-dimensional que contiene un mapa con las posiciones navegables y las que no.
        :return:  Lista 2-dimensional del  Mapa actualizado con las distancias al faro
        :return type: list

        """

        # Faro pasa de tupla a lista, y le añado distancia 0
        # (x,y) => (x,y,d) donde d es la distancia al faro.
        faro = list(faro)
        faro.append(0)
        explorar=[faro]
        while explorar:
            punto = explorar.pop(0)
            ### Aquí revisar el indice 0 y 1 o del reves, aunque tampoco importa
            if mapa[punto[1]][punto[0]] > punto[2]:
                mapa[punto[1]][punto[0]]= punto[2]
                for x in [-1,0,1]:
                    for y in [-1,0,1]:
                        explorar.append([punto[0]+y,punto[1]+x,punto[2]+1])
        return mapa
     
    def calculaDistancias(self,lighthouses, mapa):
        """
        Esta función devuelve un diccionario con la distancia
        a cada uno de los faros
        """
        d=0
        if d>0: self.log("Entro en calculaDistancias")
        distancia={}
        xMax = len(mapa[1]);
        yMax = len(mapa);
        superior = xMax + yMax # Cualquier numero que sea superior a la distancia maxima
        faros = len(lighthouses)
        """ Inicializo matriz de distancias para cada faro, 
         si es navegable: "superior"
         si no es navegable: -1 
        """
        for faro in range(len(lighthouses)):
            distancia[faro] = [[ -1 if mapa[y][x]==0 else superior for x in xrange(xMax)] for y in xrange(yMax)]

        for faro in range(len(lighthouses)):
            distancia[faro] = self.calculaDistancia(lighthouses[faro],distancia[faro])
            if d>1: self.log("Distancia["+str(faro)+"] + \n" + str(distancia[faro]))

        if d>0: self.log("Salgo de calculaDistancias")
        return distancia


    def buscafaro(self):
        """
            Busca el raro más cercano devuelve un entero.
        """
        d=0
        if d>0: self.log("Entro en buscafaro")
        if d>1:self.log("buscafaro "+str(self.state['position']))
        x, y = self.state['position']
        superior = len(self.map) + len(self.map[1])
        if d>1: self.log("superior=" + str(superior))
        distancia_minimo = superior
        minimo = -1
        if self.state["energy"] == 0:
            return random(len(self.lighthouses))
        for faro in xrange(len(self.distancias)):
            if d>2: self.logeaFaro(faro)
#            if d>2: self.log("XXXX player_num "+ str(self.player_num))
#            if d>2: self.log("XXXX faro.owner" + str(type(self.state['lighthouses']))) #[faro]['owner']))
            #if self.distancias[faro][y][x] < distancia_minimo and self.state['lighthouses'][faro]["owner"] == None:
            if ( self.distancias[faro][y][x] < distancia_minimo and 
                    self.state['lighthouses'][faro]["owner"] <> self.player_num and 
                    self.state['lighthouses'][faro]["energy"] < self.state["energy"]):
                if d>2: self.log("Entro en minimo")
                distancia_minimo =self.distancias[faro][y][x]
                minimo = faro
            if d>2: self.log("Bucle buscafaro: x= " + str(x) + " y= "+str(y) + " faro="+ str(faro) + " d= " + str(self.distancias[faro][y][x]) + " min=" + str(minimo) + " dmin=" + str(distancia_minimo)) 
        if d>0: self.log("Salgo de buscafaro")
        return minimo 

    def reduce(self):
        """
            Devuelve el movimiento que deberíamos hacer para ir al faro 
            marcado en self.objetivo
        """
        d=0
        if d>0: self.log("entro en reduce")
        x, y = self.state['position']
        if d>1: self.log("posX:" + str(x) + " posY:" + str(y) + " objetivo=" + str(self.objetivo) + " d=("+str(self.lighthouses[self.objetivo][0]) + "," + str(self.lighthouses[self.objetivo][1]) +")")
        if self.objetivo == -1:
            return(0,0)
        tDist = self.distancias[self.objetivo]
        distanciaMin = tDist[y][x] 
        xMin =0
        yMin = 0
        for xAux, yAux in itertools.product([-1,0,1],[-1,0,1]):
            if d>2: self.log("tDist[y + yAux][x+ xAux] = "+ str(tDist[y + yAux][x+ xAux]))
            if tDist[y + yAux][x+ xAux] < distanciaMin and tDist[y + yAux][x+xAux] <> -1:
                if d>2: self.log("tDist[y + yAux][x+ xAux] = "+ str(tDist[y + yAux][x+ xAux]) + "("+str(yAux)+ ","+str(xAux) + ")")
                xMin = xAux
                yMin = yAux
                distanciaMin =tDist[y + yAux][x+ xAux]
        if d>0: self.log("Salgo en reduce")
        if d>1: self.log("devuelvo (xMin=" + str(xMin) + ", yMin=" + str(yMin) + ")")
        return (xMin,yMin)

    def error(self, message, last_move):
            self.objetivo = self.buscafaro()
            xDest, yDest = self.reduce()
            return self.move(*(xDest,yDest))

    def play(self, state):
        """Jugar: llamado cada turno.
        Debe devolver una accion (jugada).
        Este es el método que hay que sobreescribir
        de interface.py"""
        d=2
        self.state = state
        cx, cy = state['position']
        self.lighthouses = dict((tuple(lh["position"]), lh)
                            for lh in state["lighthouses"])
        self.logeaEstado()
        self.logeaFaros()
        if d>1: self.log("XXXXXself.lighthouses=" + str(self.lighthouses))
        if d>1:self.log("faro [0]:" + str(self.lighthouses.values()[0]["owner"]))
        if d>1:self.log("faro [1]:" + str(self.lighthouses.values()[1]))

        if self.estado == 0:
            self.objetivo = self.buscafaro()
            self.estado = 1
        if self.estado == 1:
            xDest,yDest = self.reduce()
            if xDest == 0 and yDest ==0:
                if d>1: self.log("estoy en destino XXXX")
#                if self.lighthouses[(cx,cy)]["owner"] <> self.player_num:
                if self.lighthouses[(cx,cy)]["owner"] == None and state["energy"] <> 0:
                    if d>1: self.log("self.attack(state[energy])")
                    return self.attack(state["energy"])
                else:
                    if self.lighthouses[(cx,cy)]["owner"] == self.player_num:
                        for dest in self.lighthouses:
                            if (dest != (cx, cy) and
                                self.lighthouses[dest]["have_key"] and
                                [cx, cy] not in self.lighthouses[dest]["connections"] and
                                self.lighthouses[dest]["owner"] == self.player_num):
                                return self.connect(dest)
                    self.objetivo = self.buscafaro()
                    xDest,yDest = self.reduce()
            return self.move(*(xDest,yDest))
        return self.move(*(-1,0))   

if __name__ == "__main__":
    iface = interface.Interface(ZelaiBot)
    iface.run()
