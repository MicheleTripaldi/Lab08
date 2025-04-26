import flet as ft


from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        # TO FILL
        target_nerc = self._view._ddNerc.value
        print(f"{target_nerc}: target_nerc")  # prende l'ID di quel NERC
        target_year = self._view._txtYears.value
        print(f"{target_year}: target_year")
        target_hours = self._view._txtHours.value
        print(f"{target_hours}: target_hours")

        lista_risultati = self._model.worstCase(target_nerc, target_year, target_hours)
        print(f"lista Ristultati: {lista_risultati}")
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {self._model.persone_totali_servite_best}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hour of outage: {self._model.ore_totali}"))
        for el in lista_risultati:
            self._view._txtOut.controls.append(ft.Text(str(el)))
        self._view.update_page()
        pass


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
