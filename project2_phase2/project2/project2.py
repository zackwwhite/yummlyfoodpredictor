#!/usr/bin/python3
#for matrices later
import numpy as np

#to bring in json data
import json

#from sklearn we imports countvectorizer and tfidfTransformer to find occurances and term fequency
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

#import NearestNeighbors to find which foods are more similar
from sklearn.neighbors import NearestNeighbors

#import MultinomialNaive Bayes to predict classification
from sklearn.naive_bayes import MultinomialNB

import operator

"""
takes data from yummly.json and returns 3 lists, foods, ingredients, and cuisines
"""
def extractJSON():
	#defining path to yummly.json in docs folder
	filename = "docs/yummly.json"
	#names three lists food, ingredients, and cuisine
	food = []
	ingredients = []
	cuisine = []
	#open file as jsonfile
	with open(filename) as jsonfile:
		#name data to contain the information loaded from file
		data = json.load(jsonfile)	
		#start for loop to iterate through data
		for d in data:
			#append info from d with key 'id' to food
			food.append(d['id'])
			#append info from d with key 'ingredients' to ingredients
			ingredients.append(d['ingredients'])
			#append info from d with key 'cuisine' to cuisine
			cuisine.append(d['cuisine'])
		#end for loop
	#return lists
	return food, ingredients, cuisine


from collections import Counter

"""
converts list in a list to a string then put the string list
"""
def convertToString(ingredients):
	#name list as ingredients_string
	ingredients_String = []
	#start of for loop that iterates the elements in list
	for ingredient in ingredients:
		#convert current iter list to string, removes brackets and ', then appends it to ingredients_String list
		ingredients_String.append(str(ingredient)[1:-1].replace("'",""))
	#return list
	return ingredients_String

"""
with cuisine as a classifer, finds number of ingredient occurances per food (which turns it into a numpy matrix, find the terf frequency and inverted document frequency of each ingredient. 
Using Multinomial Naive Bayes, predict cuisine of input strings of ingredients using the tfidf matrix of ingredients.
Using the input of number of recipes to return and the count matrix of ingredients, prints N recipes closest to the input string of ingredients
"""
def findCuisineAndRecipes(foods, ingredients, cuisines, numberOfRecipes, inputIngredients):

	#converts lsit of ingredients in list to a list of strings
	ingredients_String = convertToString(ingredients)

	#initiallizes a CountVectorizer that looks at words appearing less than 50% of the time
	count_vect = CountVectorizer(max_df=.50)
	#fit and transform the list of ingredient strings into a matrix of occurances and indexes each ingredient them
	ingredient_train = count_vect.fit_transform(ingredients_String)

	#initiallize the term frequency and inverted docment frequency transformer and make sure it uses idf
	tfidf_transformer = TfidfTransformer(use_idf=True)
	#fit and transform the countvecotizer to find the tfidf of each ingredient and have them in a matrix
	ingredient_train_tf = tfidf_transformer.fit_transform(ingredient_train)

	#initiallize multinomial Naive Bayes Classifer
	gnb = MultinomialNB()
	#fit the tfidf matrix and have cuisine classify it
	gnb_fit = gnb.fit(ingredient_train_tf,cuisines)

	test = []
	test.append(inputIngredients)
	#with the input string, convert the string in to the indexes and number of occurances of the classifier above
	#then transform it with respect to the tfidf matrix above
	#this is kept here to show hwo i counted everything
	c= Counter(gnb_fit.predict(ingredient_train_tf))
	
	for k in c.keys():
		print("%s --> %d"%(k,c[k]))
	"""
	predict_counts = count_vect.transform(test)
	predict_tfidf = tfidf_transformer.transform(predict_counts)
	#print(predict_counts)
	#predict what the classifier of the input ingredients is
	predict = gnb_fit.predict(predict_tfidf)
	#return predicted classifier
	print("We think the cuisine you are making is:")
	print(predict[0])


	#set N to be the number of recipes you want
	N = numberOfRecipes
	#set radius 1
	r = 1
	#initiallize nearestNeighbors to look for N in the radius r
	neigh = NearestNeighbors(N,r)
	#fit all the occurance count into NearestNeighbor
	neigh.fit(ingredient_train)
	#finds N neighbors closest to the count matrix of the predicted string
	neighbors = neigh.kneighbors(predict_counts,return_distance=False)
	print("Here are %d recipes to make with your ingredients"%(N))
	#starts for loop of neighbors found, n is the index of neighbors
	for n in neighbors[0]:
		#prints food at index n
		print(foods[n])
	#end for loop
	"""
"""
It asks the user to input ingredients seperated by a comma and the number of recipes to return. After extracting the data from the JSON, it uses the extracted information and the inputs to print out the predicted cuisine type and the number of recipes that can are most similar due to the inputed ingredients
"""
def UserInterface():
	userIngredients = input('Type the exact ingredients you are using seperating each by a comma\nExample:romaine lettuce,black olives,grape tomatoes,garlic,pepper,purple onion,seasoning,garbanzo beans,feta cheese crumbles\n')

	numOfRecipes = input('How many recipes do you want returned?\n')
	
	foods,ingredients,cuisines = extractJSON()

	findCuisineAndRecipes(foods, ingredients, cuisines,int(numOfRecipes), str(userIngredients))
