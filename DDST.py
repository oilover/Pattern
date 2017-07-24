#coding=utf-8
from DualSim import *
from Queue import Queue
INF = 1e12

def reverseG(G):
	G2 = {}
	for u in G:
		for v in G[u]:
			if not v in G2: G2[v] = set()
			G2[v].add(u)

def match_relation(S): # Construct edge match relation 𝑆𝑒 &
# match graph 𝐺𝑚 from 𝑆
	# S is vertex match
	pass

def TopSort(G):
	indegree = {}
	for v in G: indegree[v] = 0
	Q = Queue()
	for v in G:
		for u in G[v]:
			if not u in indegree : indegree[u]=0
			indegree[u]+=1
	for u in indegree:
		if indegree[u]==0:
			Q.put(u)
	order = []
	while not Q.empty():
		u = Q.get()
		order.append(u)
		for v in G[u]:
			indegree[v]-=1
			if indegree[v]==0:
				Q.put(v)
	return order

block = {} # which connected component belong to 
CC = {} # connected component 
CC_E = {}
def D2U(G): # directed graph to undirected
	if G.type==UNDIRECTED: return G
	UG = Graph()
	for edge in G.E:
		UG.addEdge(edge);
		e = edge 
		e['from'],e['to'] = edge['to'],e['from']
		UG.addEdge(e);
	return UG

def dfs(G, u, b):
	block[u] = b
	if not b in CC:
		CC[b] = set()
	CC[b].add(u)
	for e in G[u]:
		v = e['to']
		if not v in block:
			dfs(G, v, b)

def get_connected_component(G):
	block = {}
	if G.type==DIRECTED:
		G = D2U(G)
	b = 1
	for u in G.V:
		if not u in block:
			dfs(G, u, b)
	for e in G.E:
		u = e['from']
		b = block[u]
		if not b in CC_E:
			CC_E[b] = set()
		CC_E[b].add(e['ID'])
	return CC

def In(edge, CC):
	return edge['from'] in CC and edge['to'] in CC

def edges(G, v):
	S = {e['ID'] for e in G.V[v]};

def DDST(G, Q, w): # 𝒢: graph stream,\
# 𝒬: query graph, 𝑤: window size
	Sv, sim = DualSim(Q,G)
	simE, SE, match_graph, SV = V2EMatch(Q,G,sim)
	top_order = TopSort(Q.timing_order)
	ts = {}
	for x in range(Q.NE()): ts[x] = -1e7
	rsimE = reverseG(simE)
	get_connected_component(match_graph)
	while True:
		change = False
		for cc in CC : # for every component
			for eQ in top_order:
				lim = -1e7 #lower bound
				for preEQ in Q.V2[eQ]:
					lim = max(lim, ts[preEQ])
				Min = 1e9
				for eGid in simE[eQ] & CC_E[cc]:
					eG = G.E['eGid']
					if not In(eG, CC[cc]): continue
					if eG['time'] > lim:
						Min = min(Min, eG['time'])
					else:
						simE[eQ].remove(eGid)
						rsimE[eGid].remove(eQ)
						if len(rsimE[eGid])==0:
							SE.remove(eGid)
						change = True 
				ts[eQ] = Min
			for eQ in top_order[::-1]:
				lim = INF
				for postEQ in Q.V[eQ]:
					lim = min(lim, ts[postEQ])
				Max = -INF
				for eGid in simE[eQ] & CC_E[cc]:
					eG = G.E['eGid']
					if not In(eG, CC[cc]): continue
					if eG['time'] < lim:
						Max = max(Max, eG['time'])
					else:
						simE[eQ].remove(eGid)
						rsimE[eGid].remove(eQ)
						change = True
						if len(rsimE[eGid])==0:
							SE.remove(eGid)
						change = True 
				ts[eQ] = Max

		for cc in CC : # for every component
			for u in Q.V: 
				for v in sim[u] & CC[cc]: # v is in data graph G
					OK = True
					sv = set() # if each edge incident to 𝑢 in 𝒬 corresponds to
# a distinct edge incident to 𝑣 in 𝐶𝑚
					for edge in Q.V[u]: 
						EG = simE[edge['id']] & CC_E[cc]
						cnt = len(EG)
						if cnt!=1 :  
							OK = False
							break
						for eid in EG:
							if eid in sv :
								OK = False
								break 
							eg = G.E[eid]
							if eg['from']!=v and eg['to']!=v:
								OK = False 
								break
						if not OK:
							change = True
							sim[u].remove(v)
							SV.remove(v)
							for edge in Q.V[u]: 
								simE[edge['id']] -= edges(G, v)
		if not change: break
			
	return 	sim, simE, SV, SE, match_graph




