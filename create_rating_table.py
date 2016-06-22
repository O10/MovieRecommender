import pandas as pd
import sys

datafile = 'data/recsysrules-train.csv'

if len(sys.argv) > 1:
    datafile = sys.argv[1]

data = pd.read_csv(datafile, index_col=0)

print("Loading data from " + datafile)
uniqueUsers = pd.unique(data.get("UserID"))
uniqueMovies = pd.unique(data.get("MovieID"))
uniqueTitles = pd.unique(data.get("Title"))
print("Done")

print("Data contains ", len(uniqueUsers), "unique user and", len(uniqueTitles), "unique movies")

print("Building rating table")
ratingTable = pd.DataFrame(index=uniqueUsers, columns=uniqueTitles)
for i in range(0, len(ratingTable.index)):
    currentUserRatings = data[data["UserID"] == ratingTable.index[i]].loc[:, ["UserID", "MovieID", "Rating", "Title"]]
    for j in range(0, len(ratingTable.columns)):
        currentMovie = ratingTable.columns[j]
        currentRating = currentUserRatings[currentUserRatings["Title"] == currentMovie]
        if not currentRating.empty:
            ratingTable.iloc[i, j] = currentRating.iloc[0][2]

ratingTable.fillna(0, inplace=True)
ratingTable.to_csv('data/rating_table.csv')
print("Done")
