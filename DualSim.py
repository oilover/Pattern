
import networkx as nx

def DualSim(Q, G): # Q and G are nx.MultiDiGraph
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
		for eQ in Q.edges(data=True):
			vQ, vQ2= eQ[:2]			
			for uG in sim[vQ]: # u(G) correspond to v
				OK = False
				for eG in G.out_edges(uG,data=True,keys=True): # eQ from u
					uG2 = eG[1]
					if uG2 in sim[vQ2] and \
					eG[-1]['label']==eG[-1]['label']:
						OK = True
						break
				if not OK : 
					sim[vQ].remove(uG)
					change = True
			if len(sim[vQ])==0 : return set(), {}
			v2,v = eQ[0],eQ[1]
		
			for u in sim[v]: # u(G) correspond to v
				OK = False
				for e in G.in_edges(u, data=True):
					u2 = e[0]
					if not u2 in sim[v2]: continue
			#	for u2 in set(G.predecessors(u)) & sim[v2]: # eQ to u
					#u2 = eG['from']
					if u2 in sim[v2] and e[-1]['label']==e[-1]['label']:
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
