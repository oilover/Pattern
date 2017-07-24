from Graph import *
def V2EMatch(Q, G, sim):
	simE = {}
	#Se = set()
	subgraphG = set()
	sG = Graph()
	for eQ in Q.edges():
		a = eQ[0];
		b = eQ[1];
		ID_Q = eQ['ID'];
		if not ID_Q in simE:
			simE[ID_Q] = set()
		for A in sim[a]:
			for B in G[A]:
				#B = eG['to']
				if Q[a][b]['label'] == G[A][B]['label'] and \
				B in sim[b]:					
					simE[(a,b)].add((A,B))
					subgraphG.add(A)
					subgraphG.add(B)
	sG = G.subgraph(subgraphG)				
	return simE	, subgraphG, sG