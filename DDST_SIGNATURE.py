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
	c = 0
	Hash.append(1)
	for e in Q.edges(keys=True, data=True):
		u,v = e[:2]
		Hash_e = (r[Q.node[u][Label]] - \
			r[Q.node[v][Label]] + r[e[-1][Label]] + p) % p
		if Hash[c] <= 1e18 / Hash_e:
			Hash[c] *= Hash_e
		else:
			c+=1
			Hash[c] = Hash_e 
	for v in Q.nodes():
		for i in range(1,Q.in_degree(v)+1):
			Hash
print 'asdf'