#!/usr/bin/python3

import sys
import csv

import numpy as np
from sklearn import cluster

import matplotlib
import matplotlib.pyplot as plt


"""
extracts the flavor compound data from nature.com csv file and returns it as a list of lists
"""
def extractDoc():
	#define file name
	filename = 'docs/srep00196-s2.csv'
	#open file as defined name above
	with open (filename, newline='') as csvfile:
		#use csv reader with ',' as delimiter and name it reader
		reader = csv.reader(csvfile,delimiter=',')
		#initialize empty list that will be returned
		rawIngredients = []
		#start for loop that iterates through the reader
		for row in reader:
			#if the length of the row is three then continue
			#this is due to the beginning with comments at the start
			if len(row) == 3:
				#if the row fits the criteria then append it to the list
				rawIngredients.append(row)
		#end of for loop
		#return list
		return rawIngredients

"""
Finds all unique ingredients in the data pulled from file
and filters it based on relevancy
"""
def findUniqueIngredients( csvList, compoundThreshold ):
	#initiallizes list of unique ingredients to be returned
	ingredients = []
	
	#start for loop of compounds in list
	for row in csvList:
		#define ingredient_1 as the first ingredient in the list
		ingredient_1 = row[0]
		#define ingredient_2 as the second ingredient in the list
		ingredient_2 = row[1]

		#define sharedCompound as the number of similar flavors in the the row
		#also convert the string to an int for good measure
		sharedCompound = int(row[2])

		#if the first ingredient is not in the list and the number of similar compounds is greater than 2
		#then append the first ingredient to the list 
		if ingredient_1 not in ingredients and sharedCompound > compoundThreshold:
			ingredients.append(ingredient_1)
		#end if
		#if the second ingredient is not in the list and number of similar compounds is greater than 2
		#then append the second ingredient to the list
		if ingredient_2 not in ingredients and sharedCompound > compoundThreshold:
			ingredients.append(ingredient_2)
		#end if
	#end for loop
	#after the list has been populated then return the list
	return ingredients

"""
Initializes simiarlity matrix with all zeros. matrix in n x n where n is the length of the number of unique ingredients
"""
def initiallizeSimilarityMatrix( ingredients ):
	#set ingrdient total to be the length of unique ingredients
	ingredientTotal = len(ingredients)
	#set n to be the ingredientTotal twice
	n = (ingredientTotal, ingredientTotal)
	#set a numpy matrix to be n
	SimMAT = np.zeros(n)
	#return zero matrix
	return SimMAT

"""
populate similarity matrix with values in the ingredient similarity values.
it fills the diagonals  (the same ingredient) with a 10% of the max similarity
if the flavorCompounds is less than the compoundThreshold then it is exempt
"""
def populateSimilarityMatrix( simMAT, ingredientSimilarity, ingredients, compoundThreshold):
	#finds the max of the similarity
	max_flavors = maxSimilarity(ingredientSimilarity)
	#increases the max_flavor by 10%
	max_flavors *= 1.1
	#the diagonal for simMAT with max_flavors
	np.fill_diagonal(simMAT,max_flavors)

	#for loop that iterates ingredient similarty list
	for ingSim in ingredientSimilarity:
		#converts the shared flavors to int
		sharedCompounds = int(ingSim[2])
		#if sharedCOmpounds is greater than the compoundThreshold then continue
		if sharedCompounds > compoundThreshold:
			#find Ingredient Index of the two ingredients
			index = findIngredientIndex(ingSim[0],ingSim[1],ingredients)
			#set i to the index of the first ingredient
			i = index[0]
			#set j to the index of the second ingredient
			j = index[1]
			#set i,j and j,i of the matrix to the sharedCompounds value
			simMAT[i][j] = sharedCompounds
			simMAT[j][i] = sharedCompounds

"""
finds the highest similarity in the list of ingredient similarities
the reason getListAtPos is not used is becuase this converts it to int
"""
def maxSimilarity(ingredientSimilarities):
	#creates empty list to hold the similar flavors
	maxlist = []
	#start a for loop that runs through all the ingredient similarities
	for ingredients in ingredientSimilarities:
		#convert the similiarity to int and appends it to maxlist
		maxlist.append(int(ingredients[2]))
	#finds the max in maxlist and returns it
	return max(maxlist)

"""
finds the indexes of the ingredients in the list of unique ingredients
"""
def findIngredientIndex(ingredient_1, ingredient_2, ingredientList):
	#finds the first ingredient's index
	index_1 = ingredientList.index(ingredient_1)
	#finds the second ingredient's index
	index_2 = ingredientList.index(ingredient_2)
	#sets indexes as list of indexes
	indexes = [index_1, index_2]
	#returns list indexes
	return indexes	

"""
Not used in main.py. Used so I could look at ingredients were being clustered together
"""
def writeIngredientListLabel( ingredients, labels):
	#initiate list
	indexedCompounds = []
	#set index to 0
	index = 0
	#create and open csv file named project2labal
	with open('project2label.csv','w',newline='') as csvfile:
		#set writer as a csv writer
		writer = csv.writer(csvfile)
		#write forloop that iterates through the list of unique ingreidents
		for ingredient in ingredients:
			#write the ingredient name and the cluster label at the given index
			writer.writerow([ingredient,labels[index]])
			#increment cluster
			index += 1


"""
takes unique ingredientlist and cluster labels list and plots it on a scatter plot
"""
def plotClusters(ingredients, labels):
#	matplotlib.use('Agg')
	#set fig and ax to subplots
	fig,ax = plt.subplots()
	#create xs, ys to empty list
	xs = []
	ys = []

	#sets the cluster labels in a string to be used as a label for the plot
	cluster_label = "28-parsley\n27-lavender\n26-scotch spearmint\n25-caviar\n24-roman chamomile\n23-cabbage\n22-corn mint\n21-spearmint\n20-grape fruit\n19-lemon peel\n18-peppermint\n17-orange peel\n16-mint\n15-pepper\n14-potato\n13-cocoa\n12-alcohol\n11-wheat/alcohol\n10-pork\n9-berry\n8-beans\n7-grapes\n6-fungi\n5-cheese\n4-shrimp\n3-pomme fruit\n2-tea\n1-meats\n0-citrus fruit"
	#starts for loop to length the unique ingredients
	for i in range(len(ingredients)):
		#appends i to xs
		xs.append(i)
		print("%d : %s : Cluster: %d" %(i, ingredients[i],labels[i]))
		#appends the label at point i to ys
		ys.append(labels[i])
	#makes scatter, title, x, y, grid, and puts the label on the right side
	ax.scatter(xs,ys,c=ys,label=cluster_label)
	ax.set_title("Ingredient Clustering")
	ax.set_xlabel("Ingredient")
	ax.set_ylabel("Cluster labels")
	ax.grid(True)
	ax.legend(bbox_to_anchor=(1,1))
	#shows plot
	plt.show()


