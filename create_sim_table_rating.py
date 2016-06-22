import pandas as pd
import sys
from scipy.spatial.distance import cosine

datafile = 'data/rating_table_train.csv'
if len(sys.argv) > 1:
    datafile = sys.argv[1]

ratingTable = pd.read_csv(datafile, index_col=0)

print("Calculating rating simillarities")
simillarityMatrix = pd.DataFrame(index=ratingTable.columns, columns=ratingTable.columns)

for i in range(0, len(simillarityMatrix.columns)):
    for j in range(0, len(simillarityMatrix.columns)):
        if (pd.isnull(simillarityMatrix.iloc[j, i])):
            simillarityMatrix.iloc[i, j] = 1 - cosine(ratingTable.iloc[:, i], ratingTable.iloc[:, j])
        else:
            simillarityMatrix.iloc[i, j] = simillarityMatrix.iloc[j, i]

simillarityMatrix.to_csv('data/sim_matrix_rating.csv')
print("Done")
