# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # RecSysRules 2015 - Dataset
# Script to generate train dataset for RecSysRules 2015 Challenge (Rule-based Recommender Systems for the Web of Data - 
# http://www.csw.inf.fu-berlin.de/ruleml2015/recsysrules-2015.html)
# 
# - Python Script
#   - https://s3-eu-west-1.amazonaws.com/recsysrules2015/RecSysRules2015-Dataset.py
# 
# ## Author
# Jaroslav Kuchař (Czech Technical University, Prague)
# 
# ## Description
# Train dataset for The challenge is subset of MovieLens dataset. It is a dataset provided by GroupLens Research that contains rating datasets of movies from MovieLens website. MovieLens1M with 1 million ratings from 6000 users on 4000 movies will be used for this challenge. This dataset is enriched by additional semantic information using DBpedia mappings provided by SisInf Lab. 
# 
# ## References
# - MovieLens dataset
#   - http://grouplens.org/datasets/movielens/
# - SisInf Lab mappings
#   - http://sisinflab.poliba.it/semanticweb/lod/recsys/datasets/
# - RecSysRules 2015 mappings and subset indexes
#   - https://s3-eu-west-1.amazonaws.com/recsysrules2015/RuleMLChallenge2015.zip
# - RecSysRules 2015 index of training instances
#   - https://s3-eu-west-1.amazonaws.com/recsysrules2015/train-index.zip
# - Script is inspired by 
#   - http://nbviewer.ipython.org/github/marcelcaraciolo/big-data-tutorial/blob/master/tutorial/1-Playing-with-Recommender-Systems.ipynb

# <codecell>

"""
Import modules
"""
import urllib.request, urllib.parse, urllib.error
import zipfile
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# <codecell>

"""
Download
"""
urllib.request.urlretrieve("http://files.grouplens.org/datasets/movielens/ml-1m.zip", "ml-1m.zip")
urllib.request.urlretrieve("https://s3-eu-west-1.amazonaws.com/recsysrules2015/train-index.zip", "train-index.zip")
urllib.request.urlretrieve("https://s3-eu-west-1.amazonaws.com/recsysrules2015/RuleMLChallenge2015.zip", "RuleMLChallenge2015.zip")

# <codecell>

"""
Extract
"""
with zipfile.ZipFile("ml-1m.zip", "r") as z:
    z.extractall("./")
with zipfile.ZipFile("train-index.zip", "r") as z:
    z.extractall("./")
with zipfile.ZipFile("RuleMLChallenge2015.zip", "r") as z:
    z.extractall("./")

# <codecell>

"""
Settings
"""
movieLensUsers = "./ml-1m/users.dat"
movieLensMovies = "./ml-1m/movies.dat"
movieLensRatings = "./ml-1m/ratings.dat"
recSysRulesDatatypes = "./MappingDBpedia2Movielens_datatypes.csv"
recSysRulesCategories = "./MappingDBpedia2Movielens_categories.csv"
recSysRulesTrainIndex = "./train-index.csv"

# <codecell>

"""
Import MovieLens 1M
"""
unames = ['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code']
users = pd.read_table(movieLensUsers, sep='::', header=None, names=unames)

rnames = ['UserID', 'MovieID', 'Rating', 'Timestamp']
ratings = pd.read_table(movieLensRatings, sep='::', header=None, names=rnames)

mnames = ['MovieID', 'Title', 'Genres']
movies = pd.read_table(movieLensMovies, sep='::', header=None, names=mnames)

# <codecell>

"""
MovieLens 1M Details
"""
print("Users: {0}".format(users.shape)) 
print(users.head(3))
print("Movies: {0}".format(movies.shape)) 
print(movies.head(3))
print("Ratings: {0}".format(ratings.shape)) 
print(ratings.head(3))

# <codecell>

"""
Import RecSysRules Mappings
"""
datatypes=pd.read_csv(recSysRulesDatatypes, sep=';',)
categories=pd.read_csv(recSysRulesCategories, sep=';')
datatypes.rename(columns={'title':'Title', 'id':'MovieID'},inplace=True)
categories.rename(columns={'title':'Title', 'id':'MovieID'},inplace=True)

# <codecell>

"""
RecSysRules Mappings Details 
"""
print("Datatypes: {0}".format(datatypes.shape))
print(datatypes[:3])
print("Categories: {0}".format(categories.shape)) 
print(categories[:3])

# <codecell>

"""
Load train split
"""
trainIndex = np.loadtxt(recSysRulesTrainIndex, dtype=int)
trainRatings = ratings.iloc[trainIndex]
print("RecSysRules Train Ratings: {}".format(trainRatings.shape))
print(trainRatings.head(3))

# <codecell>

"""
Merge movielens
"""
print("Users {} + Movies {} + Ratings {} ".format(users.shape, movies.shape, trainRatings.shape))
trainMovielens = pd.merge(pd.merge(trainRatings, users), movies)
print("RecSysRules Train Merged: {} \n ...".format(trainMovielens.shape))
print(trainMovielens.head(3))

# <codecell>

"""
Merge mappings
"""
print("Datatypes {} + Categories {}".format(datatypes.shape, categories.shape))
mappings = pd.merge(datatypes, categories)
print("RecSysRules Mappings Merged: {} \n ...".format(mappings.shape))
print(mappings[:3])

# <codecell>

"""
Merge all
"""
mappings.drop('Title', axis=1, inplace=True)

print("Train {} + Mappings {}".format(trainMovielens.shape, mappings.shape))
recsysrulesTrain = pd.merge(trainMovielens, mappings, left_on="MovieID", right_on="MovieID", how="inner")
print("RecSysRules All Merged: {} \n ...".format(recsysrulesTrain.shape))
print(recsysrulesTrain[:3])

# <codecell>

print("Number of unique users in test set: {}".format(len(recsysrulesTrain['UserID'].unique())))

# <codecell>

"""
Export csv
"""
recsysrulesTrain.to_csv("recsysrules-train.csv",float_format="%d")

