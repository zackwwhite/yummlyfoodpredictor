# yummlyfoodpredictorZack White
Dr. Christian Grant
Intro To Text Analytics
Project 2 Phase 1

========================PURPOSE=======================
------------------------Phase 1-----------------------
The purpose of project 2 phase 1 is to cluster the 
ingredients of the nature.com data set and then
visualize it canonical labels
======================DESCRIPTION======================
-The program extracts data from a doc that has the number of 
similarities between 2 ingredients. 
-Some of the compounds are dropped due to irrelevance.
-A list of unique ingredients is made of those that are left
-Initialize a similarity matrix of zeros
-Populate the Matrix with the info from the extracted doc
-from sklearn, use the affinity_propagation to cluster the 
similarity matrix
-get a list of the labels
-then plot a scatter chart that is cluster classification v
the index of the ingredient
-Color does indicate cluster but is really only there for readability
======================INSTALLATION=====================
Create and activate your Python3 virtual environment in the directory project2_phase1. (This program works with 3.4,3.5, and 3.6)
then do the following commands:
1. pip3 install -r requirements.txt
2. pip3 install .
3. python3 main.py (if you want to run the main program)
PLEASE READ: The requirements in phase2 are unchanged so while you can still install it and it will work. You can just install one phase and the other phase will run just fine.
=======================HOW TO RUN======================
To run the program 
python3 main.py (thats it)
=====================ASSUMPTIONS======================
------------------------Phase 1------------------------
I assumed I didn't have to download dataset since there
was nothing in the instructions that said it had to be
requested in the program. So nature.com set is in the 
docs folder

I assumed that I could filter out some of the data that
was ultimately irrelivent. With some flavors only showing
up in the 1 flavor similarity, they did not bring 
anything to the table and ultimately threw off the accuracy
of the clusters. So I threw out any compounds that was less
than 20.
	The justification for this is that I plotted a chart
of the number of unique vs the flavor threshold from 0-100 and I ploted number of clusters vs the flavor threshold from 0-100.
	The first chart showed the number of unique flavors drop dramatically then linearly decrease by 20. 20 also had a low 
cluster count. So 20 what chosen as the flavor threshold. These charts are in the same level as the README

I assumed that adding 10% to the max compound flavor and puttign it in the diagonal was good enough for the cluster to distinguish
which ingredients were the same 
======================RESOURCES============================
matplotlib documentation for scatter plot and labels

python3 for refreshing me on csv writing and reading

sklearn documentation for clustering


 =======================PROCESS==============================
-----------------------------Phase 1-----------------------
 After numerious trial and errors with experimenting with the data, 
 i went with sklearn's affinity_propagation's clustering, at Dr. Grant
 suggestion, due to its efficiency at similarity matrix
 
 The similarity matrix is built by doing the following:
 
 1.FIltering out ingredients that only appear in low flavor compounds.
 2.finding all unique ingredients afterwards and creating a list to be
	used as an index
 3.create an n x n matrix where n is the length of the list of unique 
	ingredients
 4. populate matrix with flavor compounds between ingredients, 
 5. put similarity matrix into affinity_propagation cluster.
 6. Profit
 ======================METHODS===============================
 main.py-----------------------------------------------------
 main.py imports methods from project2.py from the project2 directory.
 
 The process of main is the same as the descripton

 project2.py--------------------------------------------------
 Okay so I'm tired of going through step by step like I've done in previous
 README files in the last projects so I'm going to run through the
 methods and point out anything major import in that method that is
 worth mentioning
 
 extractDoc()
 Summary: This method extracts the information from nature.com csv dataset
			and stores each row as a list that is appended to a list that
			contains the lists
 Details: Definign the file path of docs/srep00196-s2.csv, the file is open and is then put into a csv reader. a for loop is established to read through each row, see if the row is of length 3 sicne there are comments at the beginning that throw off things off and are not relvent to the project. The list that the refined data is appended o is returned 
 
 findUniqueIngredients( csvList )
 Summary: Reads the the extracted data and finds the number of unique 
			ingredients that fit are greater than the shared flavor compound
 Details: This runs the the list found in the method above and checks to make sure that if either ingredient is not in the list of unique ingredients and the sharedCompounds is greater that the compoundThreshold, then the ingredients are put in the list. The list of unique ingredients is returned

 initiallizeSimilarityMatrix(ingredients)
 Summary: Initializes the Similarity Matrix that is the length of the number of unique ingredients found
 
 Details: With the list of unique ingredients, the number of unique ingredients is stored. Then n is set to that number twice. A numpy matrix of zeros is set The shape is n. The matrix is returned

 
populateSimilarityMatrix(simMat, ingredientSimilarity, ingredients, compoundThreshold)
 Summary:Populates the Similarity Matrix 
 
 Details: using a later method, the max similarity compound is found. It is then increased by 10% and set to the diagonal of the similarity matrix. Then looking at the ingredientSimilarity list, if the sharedCompounds are greater than the compoundThreshold, then the indexes (i,j) are found of the two ingredients and the positions of the similarity matrix i,j and j,i are set to that shareCompound value

 maxSimilarity(ingredientSimilarities)
Summary: it finds the highest compound similarities in a list

Details: First, all the compoundFlavor values in ingredientSimilarities are put in a list, then the max of those values is found and returned
 
 findIngredientIndex(ingredient_1, ingredient_2, ingredientList)
 Summary: Input two ingredients and find their index with in the list of unique ingredients and returns the indexes of ingredient_1 and ingredient_2 respectively
 Details: index_1 is set to the index found of ingredient_1 in the ingredientList. Index_2 is set to the index found of ingredient_1 in the ingredientList. Index_1 and Index_2 are put in a list and returned
 
  writeIngredientListLabel( ingredients, labels)
  SUmmary: I wrote this method to make a csv file for me to look over the data. It isn't used in main.py but I'm leaving it here to show how I was looking at things
  Details:  This jsut writes the ingredient with its corresponding cluster label and puts them in a csv

plotCluster(ingredients, labels)
Summary: Plots the ingredients and clsuters in a scatter plot. The x axis is the ingredient indexes and the y axis is the clsuter label

Summary:Set up a subplot. Then a string is defined with all the labels. The index of the unique ingredients list is put in xs and the labels are put into ys. A scatter plot is made with the title "Ingredient Clustering. X axis labeled Ingredient and y axis CLuster Labels. A grid is set and the legned is set outside to the right. The plot is then showed. For COnvience. The index and the corresponding ingredient are printed out.
