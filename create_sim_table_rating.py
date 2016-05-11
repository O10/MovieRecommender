import pandas as pd
from scipy.spatial.distance import cosine

ratingTable = pd.read_csv('data/rating_table.csv', index_col=0)

print("Calculating rating simillarities")
simillarityMatrix = pd.DataFrame(index=ratingTable.columns, columns=ratingTable.columns)

for i in range(0, len(simillarityMatrix.columns)):
    for j in range(0, len(simillarityMatrix.columns)):
        simillarityMatrix.iloc[i, j] = 1 - cosine(ratingTable.iloc[:, i], ratingTable.iloc[:, j])

simillarityMatrix.to_csv('data/sim_matrix_rating.csv')
print("Done")
