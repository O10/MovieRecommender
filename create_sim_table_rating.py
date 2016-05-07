import pandas as pd
from scipy.spatial.distance import cosine

ratingTable = pd.read_csv('data/rating_table.csv', index_col=0)

print("Calculating simillarities")
simillarityMatrix = pd.DataFrame(index=ratingTable.columns, columns=ratingTable.columns)

for i in range(0, len(simillarityMatrix.columns)):
    for j in range(0, len(simillarityMatrix.columns)):
        simillarityMatrix.iloc[i, j] = 1 - cosine(ratingTable.iloc[:, i], ratingTable.iloc[:, j])

print("Done")

print("Finding and printing best matches")

dataNeighbours = pd.DataFrame(index=simillarityMatrix.columns, columns=range(1, 11))

for i in range(0, len(simillarityMatrix.columns)):
    dataNeighbours.iloc[i, :10] = simillarityMatrix.iloc[:, i].order(ascending=False)[0:10].index

dataNeighbours.to_csv('data/sim_table_rating.csv')
simillarityMatrix.to_csv('data/sim_matrix_rating.csv')
print("Done")
