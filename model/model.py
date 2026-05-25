import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()


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
                        if numTracceU[0] > numTracceV[0]:
                            self._grafo.add_edge(u, v, weight=numTracceU[0]+numTracceV[0])
                        elif numTracceU[0] < numTracceV[0]:
                            self._grafo.add_edge(v, u, weight=numTracceU[0]+numTracceV[0])
                        elif numTracceU[0] == numTracceV[0]:
                            self._grafo.add_edge(u, v, weight=numTracceU[0]+numTracceV[0])
                            self._grafo.add_edge(v, u, weight=numTracceU[0]+numTracceV[0])

    def getArtistaInfluente (self):
        artista_influente = None
        influenza = 0
        for artista in self._grafo.nodes:
            outW = self._grafo.out_degree[artista]
            inW = self._grafo.in_degree[artista]

            influenzaArtista = outW - inW
            if influenzaArtista >influenza:
                influenza = influenzaArtista
                artista_influente = artista
        return artista_influente

    def getPrimi5(self):
        Primi5 = sorted(
            self._grafo.edges(data=True),
            key=lambda x: x[2].get("weight", 0),
            reverse=True
        )[:5]
        return Primi5