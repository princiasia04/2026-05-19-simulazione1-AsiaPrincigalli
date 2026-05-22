import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph
        self.artista_influente = None
        self.influenza = 0

    def getGeneri (self):
        return DAO.getGeneri()

    def creaGrafo (self, genere):
        artisti = DAO.getArtisti(genere)
        self._grafo.add_nodes_from(artisti)
        artista_clienti = {}
        for artista in artisti:
            listaClienti = DAO.getClienti(artista)
            artista_clienti[artista] = listaClienti

        for u in self._grafo.nodes:
            for v in self._grafo.nodes:
                if u != v:
                    clientiU = artista_clienti[u]
                    clientiV = artista_clienti[v]
                    if set(clientiU) & set(clientiV):
                        numTracceU = DAO.getNumeroTracce(u)
                        numTracceV = DAO.getNumeroTracce(v)
                        if numTracceU > numTracceV:
                            self._grafo.add_edge(u, v, weight=numTracceU+numTracceV)
                        elif numTracceU < numTracceV:
                            self._grafo.add_edge(v, u, weight=numTracceU+numTracceV)
                        elif numTracceU == numTracceV:
                            self._grafo.add_edge(u, v, weight=numTracceU+numTracceV)
                            self._grafo.add_edge(v, u, weight=numTracceU+numTracceV)

    def getArtistaInfluente (self):
        for artista in self._grafo.nodes:
            influenzaArtista = self._grafo.out_degree(artista) - self._grafo.in_degree(artista)
            if influenzaArtista >self.influenza:
                self.artista_influente = artista
        return self.artista_influente

    def getPrimi5(self):
        Primi5 = sorted(
            self._grafo.edges(data=True),
            key=lambda x: x[2].get("weight", 0),
            reverse=True
        )[:5]
        return Primi5