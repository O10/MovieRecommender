import pandas as pd

goodMovieTreshold = 4

ratingTable = pd.read_csv('data/rating_table.csv', index_col=0)
movieTable = pd.read_csv('data/movie_table.csv', index_col=0)
movieTable.drop(movieTable.columns[0:19], axis=1, inplace=True)

print("Creating features table")
featureMatrix = pd.DataFrame(0, index=ratingTable.index, columns=movieTable.columns, )

for i in range(0, len(featureMatrix.index)):
    s = ratingTable.loc[featureMatrix.index[i], :]
    userHighRankedMovies = s[s >= goodMovieTreshold]

    for j in userHighRankedMovies.index:
        featureMatrix.iloc[i, :] += movieTable.loc[j, :]

featureMatrix.to_csv('data/feature_matrix.csv')
print("Done")
