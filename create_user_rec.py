import pandas as pd

print("Loading data")

ratingTable=pd.read_csv('data/rating_table.csv')
dataNeighbours=pd.read_csv('data/sim_table_rating.csv')
simillarityMatrix=pd.read_csv('data/sim_matrix_rating.csv')

print("Done")

def getScore(history, similarities):
   return sum(history*similarities)/sum(similarities)

print("Calculating each user top 5 recommendations")

data_sims = pd.DataFrame(index=ratingTable.index,columns=ratingTable.columns)

for i in range(0,len(data_sims.index)):
    for j in range(0,len(data_sims.columns)):
        user = data_sims.index[i]
        product = data_sims.columns[j]

        if ratingTable.iloc[i][j] > 0:
            data_sims.iloc[i][j] = 0
        else:
            product_top_names = dataNeighbours.ix[product][1:10]
            product_top_sims = simillarityMatrix.ix[product].order(ascending=False)[1:10]
            user_purchases = ratingTable.ix[user,product_top_names]
            data_sims.iloc[i][j] = getScore(user_purchases,product_top_sims)

dataRecommend = pd.DataFrame(index=data_sims.index, columns=range(1, 6))

for i in range(0,len(data_sims.index)):
    dataRecommend.ix[i, 0:]= data_sims.iloc[i, :].order(ascending=False).iloc[0:5, ].index.transpose()

dataRecommend.to_csv('data/user_recomendations.csv')
print("Done")