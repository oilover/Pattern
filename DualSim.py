
import networkx as nx

def DualSim(Q, G):
	sim = {}
	for v in Q.V:
		sim[v] = set()
		for u in G.V:
			if Q.label[u]==G.label[v]:
				sim[v].add(u)
	while True:
		change = False
		for eQ in Q.E:
			vQ = eQ['from']
			vQ2 = eQ['to']
			for uG in sim[vQ]: # u(G) correspond to v
				OK = False
				for eG in G.V[uG]: # eQ from u
					uG2 = eG['to']
					if uG2 in sim[vQ2] and eG['label']==eQ['label']:
						OK = True
						break
				if not OK : 
					sim[vQ].remove(uG)
					change = True
			if len(sim[vQ])==0 : return set()
			v2 = eQ['from']
			v = eQ['to']
			for u in sim[v]: # u(G) correspond to v
				OK = False
				for eG in G.V2[u]: # eQ to u
					u2 = eG['from']
					if u2 in sim[v2] and eG['label']==eQ['label']:
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
