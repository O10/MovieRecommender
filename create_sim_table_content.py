import pandas as pd
from scipy.spatial.distance import cosine

movieTable = pd.read_csv('data/movie_table.csv', index_col=0)

movieTable.drop(movieTable.columns[0:19], axis=1, inplace=True)

print("Calculating content simillarities")
simillarityMatrix = pd.DataFrame(index=movieTable.index, columns=movieTable.index)

for i in range(0, len(simillarityMatrix.columns)):
    for j in range(0, len(simillarityMatrix.columns)):
        simillarityMatrix.iloc[i, j] = 1 - cosine(movieTable.iloc[i, :], movieTable.iloc[j, :])

simillarityMatrix.to_csv('data/sim_matrix_content.csv')
print("Done")
