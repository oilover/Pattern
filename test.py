
import networkx as nx
import matplotlib.pyplot as plt
'''
petersen=nx.petersen_graph()
tutte=nx.tutte_graph()
maze=nx.sedgewick_maze_graph()
tet=nx.tetrahedral_graph()

#nx.draw(petersen)
G = nx.karate_club_graph()

nx.draw_spectral(G)
'''
Lim = 1e18
def ADD(List, c):
	if len(List)==0 or List[-1] > Lim / c: List.append(c)
	else : List[-1]*=c 
    
T = []
ADD(T,54)
ADD(T, 23)
print T