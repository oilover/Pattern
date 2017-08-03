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


def dfs(G, u, b):
	block[u] = b
	if not b in CC:
		CC[b] = set()
	CC[b].add(u)
	for v in G[u]:		
		if not v in block:
			dfs(G, v, b)

def get_connected_component(G):
	block = {}
	if G.is_directed():
		G = G.to_undirected()
	b = 1
	for u in G:
		if not u in block:
			dfs(G, u, b)
	for e in G.edges():
		u = e[0]
		b = block[u]
		if not b in CC_E:
			CC_E[b] = set()
		CC_E[b].add(e)
#	return CC

def In(edge, CC):
	return edge[0] in CC and edge[1] in CC


def E2G(E): # Construct Graph from set of edges(pair) 
	G = {}
	for e in E:
		u , v = e[0], e[1]
		if not u in G:
			G[u] = set()
		G[u].append(v)
	return G

def DDST(G, timing_order, Q): # 𝒢: graph stream,\
# 𝒬: query graph, 𝑤: window size
	sim = DualSim(Q, G)
	simE, match_graph = V2EMatch(Q,G,sim)
	top_order = TopSort(timing_order)
	ts = {}
	for x in Q.edges(): ts[x] = -INF
	rsimE = reverseG(simE)
	get_connected_component(match_graph)
	timing_graph = E2G(timing_order)
	for v in Q.edges() : 
		if not v in timing_graph: timing_graph[v]=set()
	rev_timing_graph = reverseG(timing_graph)
	for v in Q.edges() : 
		if not v in rev_timing_graph: rev_timing_graph[v]=set()
	while True:
		change = False
		for cc in CC : # for every component
			for eQ in top_order:
				lim = -1e7 #lower bound
				for preEQ in rev_timing_graph[eQ]:
					lim = max(lim, ts[preEQ])
				Min = 1e9
				for eG in simE[eQ] & CC_E[cc]:
				#	eG = G.E['eGid']
					if not In(eG, CC[cc]): continue
					if G[eG[0]][eG[1]]['time'] > lim:
						Min = min(Min, eG['time'])
					else:
						simE[eQ].remove(eG)
						rsimE[eG].remove(eQ)
						if len(rsimE[eGid])==0:
							SE.remove(eGid)
						change = True 
				ts[eQ] = Min
			for eQ in top_order[::-1]:
				lim = INF
				for postEQ in timing_graph[eQ]:
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


