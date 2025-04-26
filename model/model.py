import copy
from datetime import datetime

from database.DAO import DAO
from model import nerc
from model.powerOutages import Event



class Model:
    def __init__(self):
        self._solBest = []

        self.persone_totali_servite_best = 0
        self.ore_totali = 0

        self._listNerc = None
        self._listEvents = None
        self.loadNerc()


    def worstCase(self, nerc, maxY, maxH):
        # TO FILL
        self._solBest = []
        self.lista_tutte_soluzioni_possibili = []

        self.persone_totali_servite_best = 0
        self.ore_totali = 0

        self._listNerc = None
        self._listEvents = None

        self.loadEvents(nerc)
        lista_eventi_totali_nerc = self._listEvents
        print("---------------------")
        print(f"lista eventi totali nerc: {lista_eventi_totali_nerc}")
        print("--------------")
        self.ricorsione([], maxY, maxH, lista_eventi_totali_nerc)
        return self._solBest



    def ricorsione(self, parziale, maxY, maxH, lista_eventi):
        # TO FILL
        # in ingresso ho la lista della soluzione parziale
        # il massimo di anni
        # il massimo di ore totali
        # l' insieme di tutti gli eventi della regione

        # ho una variabile globale che mi memorizza la lista di tutte le possibili soluzioni
        if len(lista_eventi) == 0:
            print(f"Una sequenza possibile può essere:{parziale}")
            self.lista_tutte_soluzioni_possibili.append(copy.deepcopy(parziale))
            tot_persone = self.calcola_persone(parziale)
            print(f"costo di tale soluzione vale = {tot_persone}")

            if tot_persone > self.persone_totali_servite_best:
                self.persone_totali_servite_best = tot_persone
                self._solBest = copy.deepcopy(parziale)
                self.ore_totali = self.calcola_ore(parziale)

        #condizione ricorsiva
        else:
            for evento in lista_eventi:
                if self.is_admissible(parziale, maxY, maxH, evento):
                    nuova_lista_eventi = copy.deepcopy(lista_eventi)
                    nuova_lista_eventi.remove(evento)
                    parziale.append(evento)
                    self.ricorsione(parziale, maxY, maxH, nuova_lista_eventi)
                    parziale.pop()

    def is_admissible(self, parziale, maxY, maxH, evento):
        #vincolo sugli anni
        anno_max = 0
        anno_min = 0
        step = 1
        nuova_lista = parziale +[evento]
        for event_i in nuova_lista:
            if step == 1:
                anno_min = event_i.date_event_began.year
                anno_max = event_i.date_event_finished.year
                step = 2
            if event_i.date_event_began.year < anno_min:
                anno_min = event_i.date_event_began.year
            if event_i.date_event_finished.year > anno_max:
                anno_max = event_i.date_event_finished.year
        if (anno_max - anno_min) > (int(maxY)):
            print(f"{anno_max}-{anno_min} > int({maxY})")
            print(f"LA DIFFERENZA DEGLI ANNI SUPERA IL LIMITE DI ANNI, NON AGGIUNGO QUESTO EVENTO: {evento.id}")
            return False

        # vincolo sulle ore
        conta_ore = self.calcola_ore(nuova_lista)

        if conta_ore > int(maxH):
            print(f"{conta_ore} > {maxH} → TROPPO TEMPO, NON AGGIUNGO")
            return False

        return True

    def calcola_ore(self, parziale):
        conta_ore = 0
        for event_i in parziale:
            conta_ore += (event_i.date_event_finished - event_i.date_event_began).total_seconds()
        return conta_ore / 3600

    def calcola_persone(self, parziale):
        conta_clienti = 0
        for evento in parziale:
            conta_clienti = conta_clienti + evento.customers_affected
        return conta_clienti




    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc