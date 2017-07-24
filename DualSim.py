
import networkx as nx

def DualSim(Q, G): # Q and G are nx.DiGraph
	sim = {}
	for v in Q:
		sim[v] = set()
		for u in G.V:
			if Q.node[u]['label']==G.node[v]['label']:
				sim[v].add(u)
	Q2 = Q.reverse()
	G2 = G.reverse()
	while True:
		change = False
		for eQ in Q.edges():
			vQ = eQ[0]
			vQ2 = eQ[1]
			for uG in sim[vQ]: # u(G) correspond to v
				OK = False
				for uG2 in G[uG]: # eQ from u
					uG2 = eG['to']
					if uG2 in sim[vQ2] and G[uG][uG2]['label']==Q[vQ][vQ2]['label']:
						OK = True
						break
				if not OK : 
					sim[vQ].remove(uG)
					change = True
			if len(sim[vQ])==0 : return set(), {}
			v2,v = eQ[0],eQ[1]
		
			for u in sim[v]: # u(G) correspond to v
				OK = False
				for u2 in set(G2[u].keys()) & sim[v2]: # eQ to u
					#u2 = eG['from']
					if u2 in sim[v2] and G[u2][u]['label']==Q[v2][v]['label']:
						OK = True
						break
				if not OK : 
					sim[v].remove(u)
					change = True
			if len(sim[v])==0 : return set()
		if not change: break

		
	Sv = set()
	for v in Q.V:
		for u in sim[v]:
			Sv.add((v,u))
	return Sv, sim
