import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        #chiamo funzione nel model
        generi = self._model.getGeneri()
        generiDD = list(map(lambda x: ft.dropdown.Option(x), generi))
        self._view._ddGenre.options = generiDD
        self._view.update_page()

    def handleCreaGrafo(self, e):
        if self._view._ddGenre.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un genere dal menu", color="red"))
        self._model.creaGrafo(self._view._ddGenre.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Per il genere {self._view._ddGenre.value} ci sono {len(self._model._grafo.nodes)} nodi e {len(self._model._grafo.edges)} archi", color="green"))
        artistaInfluente, influenza = self._model.getArtistaInfluente()
        self._view.txt_result.controls.append(ft.Text(f"L'artista più influente è {artistaInfluente} con influenza {influenza}", color="green"))
        primi5 = self._model.getPrimi5()
        self._view.txt_result.controls.append(ft.Text("I primi 5 archi con peso peso maggiore sono:", color="green"))
        for u, v, data in primi5:
            self._view.txt_result.controls.append(ft.Text(f"{u}, {v}, {data['weight']}", color="green"))
        self._view.update_page()

    def handleGenreSelection(self, e):
        self.fillDDArtist()

    def fillDDArtist(self):
        genere = self._view._ddGenre.value
        artisti = self._model.getArtisti(genere)
        artistiDD = list(map(lambda x: ft.dropdown.Option(x), artisti))
        self._view._ddArtist.options = artistiDD
        self._view.update_page()

    def handleCammino(self,e):
        if self._view._ddArtist.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un artista dal menu", color="red"))
        nodoPartenza = self._view._ddArtist.value
        migliorCammino = self._model.getCammino(nodoPartenza)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Miglior cammino trovato! Stampo percorso", color="green"))
        for nodo in migliorCammino:
            self._view.txt_result.controls.append(ft.Text(f"{nodo}", color="green"))
        self._view.update_page()