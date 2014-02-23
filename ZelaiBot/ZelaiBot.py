#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys
import interface
import copy # para copiar listas


def logFun(ident, message, *args):
    """Mostrar mensaje de registro por stderr"""
    print >>sys.stderr, "[%s] %s" % (ident, (message % args))


def calculaDistancia(faro,mapa):
    """
    Esta función defuelve las distancias de un mapa
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
#   for linea in mapa:
#       logFun("calculaDistancia",str(linea))
    return mapa
        
def calculaDistancias(lighthouses, mapa):
    """
    Esta función devuelve un diccionario con la distancia
    a cada uno de los faros
    """
    d=0
    if d>0: logFun("Entro en calculaDistancias","")
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
        distancia[faro] = calculaDistancia(lighthouses[faro],distancia[faro])
        if d>1: logFun("d","Distancia["+str(faro)+"] + \n" + str(distancia[faro]))

    if d>0: logFun("Salgo de calculaDistancias","")
    return distancia

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

        :meth: interface.Bot.__init__
        """
        # llamada a super para inicializar las variables (self.)
        #  player_num, player_count, position, map, lighthouses
        d=0
        if d>0: self.log("Entro en __init__")
        interface.Bot.__init__(self,init_state) 

        #self.log(str(self.map))
        if d>1: self.log("lighthouses:\n" + str(self.lighthouses));
        #self.log("len(lighthouses)=%d\n" %  (len(self.lighthouses)) );
        
        # posiciones validas map[0][0] - map[17,20]
        # modo de acceso map[y][x]
        self.distancias = calculaDistancias(self.lighthouses,self.map) 
        #self.log("len(lighthouses)="+ str(len(self.lighthouses)) + "\n" +str(self.distancias[0]))
        
        self.estado = 0
        self.destino = 0
        
        if d>0: self.log("Salgo en __init__")

    def buscafaro(self):
        """
            Busca el raro más cercano
            devuelve un entero.
        """
        d=0
        if d>0: self.log("Entro en buscafaro")
        if d>1:self.log("buscafaro "+str(self.position))
        x, y = self.position
        superior = len(self.map) + len(self.map[1])
        if d>1: self.log("superior=" + str(superior))
        distancia_minimo = superior
        minimo = -1
        for faro in xrange(len(self.distancias)):
            if self.distancias[faro][y][x] < distancia_minimo:
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
        x, y = self.position
        if d>1: self.log("posX:" + str(x) + " posY:" + str(y) + " objetivo=" + str(self.objetivo) + " d=("+str(self.lighthouses[self.objetivo][0]) + "," + str(self.lighthouses[self.objetivo][1]) +")")
        tDist = self.distancias[self.objetivo]
        distanciaMin = tDist[y][x] 
        xMin =0
        yMin = 0
        for xAux in [-1,0,1]:
            for yAux in[-1,0,1]:
                if d>2: self.log("tDist[y + yAux][x+ xAux] = "+ str(tDist[y + yAux][x+ xAux]))
                if tDist[y + yAux][x+ xAux] < distanciaMin and tDist[y + yAux][x+xAux] <> -1:
                    if d>2: self.log("tDist[y + yAux][x+ xAux] = "+ str(tDist[y + yAux][x+ xAux]) + "("+str(yAux)+ ","+str(xAux) + ")")
                    xMin = xAux
                    yMin = yAux
                    distanciaMin =tDist[y + yAux][x+ xAux]
        if d>0: self.log("Salgo en reduce")
        if d>1: self.log("devuelvo (xMin=" + str(xMin) + ", yMin=" + str(yMin) + ")")
        return (xMin,yMin)

                
    def play(self, state):
        """Jugar: llamado cada turno.
        Debe devolver una accion (jugada).
        Este es el método que hay que sobreescribir
        de interface.py"""
        self.position = state['position']
        self.state = state
        cx, cy = state['position']
        lighthouses = dict((tuple(lh["position"]), lh)
                            for lh in state["lighthouses"])

        if self.estado == 0:
            self.objetivo = self.buscafaro()
            self.estado = 1
        if self.estado == 1:
            xDest,yDest = self.reduce()
            if xDest == 0 and yDest ==0:
                self.log("estoy en destino XXXX")
                if lighthouses[(cx,cy)]["owner"] <> self.player_num:
                    return self.attack(state["energy"])
            return self.move(*(xDest,yDest))
            
        return self.move(*(-1,0))   

if __name__ == "__main__":
    iface = interface.Interface(ZelaiBot)
    iface.run()
