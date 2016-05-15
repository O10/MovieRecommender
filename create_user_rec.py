import pandas as pd

print("Loading data for recommendations")

ratingTable = pd.read_csv('data/rating_table.csv', index_col=0)
simillarityMatrixRating = pd.read_csv('data/sim_matrix_rating.csv', index_col=0)
simillarityMatrixContent = pd.read_csv('data/sim_matrix_content.csv', index_col=0)
featureMatrix = pd.read_csv('data/feature_matrix.csv', index_col=0)
movieTable = pd.read_csv('data/movie_table.csv', index_col=0)
movieTable.drop(movieTable.columns[0:19], axis=1, inplace=True)

rec_number = 5
topFeaturePar = 0.2
topFeatureNum = 5
simRatPar = 1
simConPar = 1

print("Done")


def getScore(history, similarities):
    return sum(history * similarities) / sum(similarities)


def getTopSimillarities(data, movie, start, stop):
    return data.loc[:, movie].order(ascending=False)[start:stop].index


print("Calculating each user top recommendations")

userSimillarities = pd.DataFrame(index=ratingTable.index, columns=ratingTable.columns)

for i in range(0, len(userSimillarities.index)):
    user = userSimillarities.index[i]
    userTopFeatures = featureMatrix.loc[user].order(ascending=False)[0:topFeatureNum].index

    for j in range(0, len(userSimillarities.columns)):
        product = userSimillarities.columns[j]

        if ratingTable.iloc[i][j] > 0:
            userSimillarities.iloc[i][j] = 0
        else:
            # rating
            ratingProductTopNames = getTopSimillarities(simillarityMatrixRating, product, 1, rec_number + 1)
            ratingProductTopSims = simillarityMatrixRating.ix[product].order(ascending=False)[1:rec_number + 1]
            ratingUserRateHistory = ratingTable.ix[user, ratingProductTopNames]

            # content
            contentProductTopNames = getTopSimillarities(simillarityMatrixContent, product, 1, rec_number + 1)
            contentProductTopSims = simillarityMatrixContent.ix[product].order(ascending=False)[1:rec_number + 1]
            contentUserRateHistory = ratingTable.ix[user, contentProductTopNames]

            # feature
            movieFeaturesScore = sum(movieTable.loc[product][userTopFeatures]) * topFeaturePar

            userSimillarities.iloc[i][j] = simRatPar * getScore(ratingUserRateHistory,
                                                                ratingProductTopSims) + simConPar * getScore(
                contentUserRateHistory, contentProductTopSims)

dataRecommend = pd.DataFrame(index=userSimillarities.index, columns=range(1, rec_number + 1))

for i in range(0, len(userSimillarities.index)):
    dataRecommend.iloc[i, 0:] = userSimillarities.iloc[i, :].order(ascending=False).iloc[
                                0:rec_number, ].index.transpose()

dataRecommend.to_csv('data/user_recomendations.csv')
print("Done")
