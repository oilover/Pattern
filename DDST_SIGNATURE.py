# encoding=utf-8
'''
Input: 𝒢: graph stream, 𝒬: query graph, 𝑤: window size
Output: match graphs of 𝒬 in 𝒢
'''
import matplotlib.pyplot as plt
import random

Label = 'label'
r = {}
p = 9857 # Prime number
Lim = 1e18
def ADD(List, c):
	if len(List)==0 or List[-1] > Lim / c: List.append(c)
	else : List[-1]*=c 

def LB(Q,v):
	return Q.node[v][Label]

Hash = []
def preprocess(Q):
	r = {}
	Hash = [1]
	for v in Q.nodes():
		l = Q.node[v][Label]
		if not l in r:
			r[l] = random.randint(0,p-1)
	for e in Q.edges(data=True):
		l = e[-1][Label]
		if not l in r:
			r[l] = random.randint(0,p-1)
	
	Hash.append(1)
	for e in Q.edges(keys=True, data=True):
		u,v = e[:2]
		he = (r[Q.node[u][Label]] - \
			r[Q.node[v][Label]] + r[e[-1][Label]] + p) % p
		ADD(Hash, he)
	for v in Q.nodes():
		for i in range(1,Q.in_degree(v)+1):
			ADD(Hash, (r[Q.node[v][Label]] + i) % p)
		for i in range(1,Q.out_degree(v)+1):
			ADD(Hash, (r[Q.node[v][Label]] - i) % p)

def Signature():
	s = [1 for i in range(len(Hash))]
	outNum = {}
	inNum = {}
	for e in G.edges(keys=True, data=True):
		u,v = e[:2]
		if not u in outNum: outNum[u]=1
		else: outNum[u] += 1
		if not v in inNum: inNum[v]=1 
		else: inNum[v] += 1 
		s_e = (r[LB(G,u)] - r[LB(G,v)] + r[e[-1][Label]]) % p 
		s_u = (r[LB(G,u)] - outNum[u]) % p
		s_v = (r[LB(G,v)] + inNum[v]) % p 
		for i in range(len(s)):
			s[i] = s[i]*s_e*s_u*s_v % Hash[i]
		OK = True 
		for x in s : 
			if x!=0 : OK=False
		if OK:
			print 'Find a match in last window'

if __name__ == '__main__':