#!/usr/bin/python3

import project2
from project2 import project2 as p2

from sklearn import cluster

def main():
	#define threshold justified in README
	threshold = 20
	#set compounds to a list of lists extracted from the doc
	compounds = p2.extractDoc()
	#set ingredients to the list of unique ingredients
	ingredients = p2.findUniqueIngredients(compounds,threshold)
	#initialize Similiarty Matrix of zeros that is n x n where n is the length of ingredients
	simMAT = p2.initiallizeSimilarityMatrix(ingredients)
	#populated the similarty ingredients
	p2.populateSimilarityMatrix( simMAT, compounds, ingredients, threshold )
	#set af tp cluster the Similarity Matrix
	af = cluster.affinity_propagation(simMAT)
	#set labels to be the list of clusters that is in order of the unique ingredients
	_, labels = af
	#plot it
	p2.plotClusters(ingredients, labels)

if __name__ == '__main__':
	main()
