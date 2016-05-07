import pandas as pd

print("Loading data")

ratingTable = pd.read_csv('data/rating_table.csv', index_col=0)
dataNeighbours = pd.read_csv('data/sim_table_rating.csv', index_col=0)
simillarityMatrix = pd.read_csv('data/sim_matrix_rating.csv', index_col=0)

print("Done")


def getScore(history, similarities):
    return sum(history * similarities) / sum(similarities)


print("Calculating each user top 5 recommendations")

userSimillarities = pd.DataFrame(index=ratingTable.index, columns=ratingTable.columns)

for i in range(0, len(userSimillarities.index)):
    for j in range(0, len(userSimillarities.columns)):
        user = userSimillarities.index[i]
        product = userSimillarities.columns[j]

        if ratingTable.iloc[i][j] > 0:
            userSimillarities.iloc[i][j] = 0
        else:
            productTopNames = dataNeighbours.ix[product][1:10]
            productTopSims = simillarityMatrix.ix[product].order(ascending=False)[1:10]
            userRateHistory = ratingTable.ix[user, productTopNames]
            userSimillarities.iloc[i][j] = getScore(userRateHistory, productTopSims)

dataRecommend = pd.DataFrame(index=userSimillarities.index, columns=range(1, 6))

for i in range(0, len(userSimillarities.index)):
    dataRecommend.ix[i, 0:] = userSimillarities.iloc[i, :].order(ascending=False).iloc[0:5, ].index.transpose()

dataRecommend.to_csv('data/user_recomendations.csv')
print("Done")
