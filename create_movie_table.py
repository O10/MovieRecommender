import pandas as pd
import sys

datafile = 'data/recsysrules-train.csv'
if len(sys.argv) > 1:
    datafile = sys.argv[1]

data = pd.read_csv(datafile, index_col=0)
uniqueMovies = pd.unique(data.get("Title"))

print("Creating movie table")
movieTable = pd.DataFrame(index=uniqueMovies, columns=data.columns)
for i in range(0, len(movieTable.index)):
    currentMovie = movieTable.index[i]
    currentMovieData = data[data['Title'] == currentMovie].iloc[0][:]
    movieTable.iloc[i][:] = currentMovieData

movieTable.to_csv('data/movie_table.csv')
print("Done")
