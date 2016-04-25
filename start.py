import pandas as pd
from scipy.spatial.distance import cosine


data = pd.read_csv('data/test.csv')
print("Loading data")
#data=pd.read_csv('data/recsysrules-train.csv') #actual data
uniqueUsers= pd.unique(data.get("UserID"))
uniqueMovies = pd.unique(data.get("MovieID"))
uniqueTitles =pd.unique(data.get("Title"))
print("Done")

print("Data contains ",len(uniqueUsers) ,"unique user and",len(uniqueTitles), "unique movies")

print("Building rating table")
ratingTable=pd.DataFrame(index=uniqueUsers,columns=uniqueTitles)
for i in range(0,len(ratingTable.index)):
    currentUserRatings=data[data["UserID"]==ratingTable.index[i]].loc[:,["UserID","MovieID","Rating","Title"]]
    for j in range(0,len(ratingTable.columns)):
        currentMovie=ratingTable.columns[j]
        currentRating=currentUserRatings[currentUserRatings["Title"]==currentMovie]
        if not currentRating.empty:
            ratingTable.iloc[i,j]=currentRating.iloc[0][2]

ratingTable.fillna(0,inplace=True)
print("Done")

print("Calculating simillarities")
simillarityMatrix = pd.DataFrame(index=ratingTable.columns,columns=ratingTable.columns)

for i in range(0,len(simillarityMatrix.columns)) :
    for j in range(0,len(simillarityMatrix.columns)) :
      simillarityMatrix.iloc[i,j] = 1-cosine(ratingTable.iloc[:,i],ratingTable.iloc[:,j])

print("Done")

print("Finding and printing best matches")

data_neighbours = pd.DataFrame(index=simillarityMatrix.columns,columns=range(1,11))

for i in range(0,len(simillarityMatrix.columns)):
    data_neighbours.iloc[i,:10] = simillarityMatrix.iloc[:,i].order(ascending=False)[0:10].index

#print(data_neighbours.head(6).iloc[:6,0:4])

##new
# Helper function to get similarity scores
def getScore(history, similarities):
   return sum(history*similarities)/sum(similarities)

# Create a place holder matrix for similarities, and fill in the user name column
data_sims = pd.DataFrame(index=ratingTable.index,columns=ratingTable.columns)

#Loop through all rows, skip the user column, and fill with similarity scores
for i in range(0,len(data_sims.index)):
    for j in range(0,len(data_sims.columns)):
        user = data_sims.index[i]
        product = data_sims.columns[j]

        if ratingTable.iloc[i][j] > 0:
            data_sims.iloc[i][j] = 0
        else:
            # print("Product is",product)
            # wait = input("PRESS ENTER TO CONTINUE.")
            product_top_names = data_neighbours.ix[product][1:10]
            # print("Product top",product_top_names)
            # wait = input("PRESS ENTER TO CONTINUE.")
            product_top_sims = simillarityMatrix.ix[product].order(ascending=False)[1:10]
            # print("Product top sims",product_top_sims)
            # wait = input("PRESS ENTER TO CONTINUE.")
            user_purchases = ratingTable.ix[user,product_top_names]
            # print("User scores",user_purchases)
            # wait = input("PRESS ENTER TO CONTINUE.")
            # print(sum(user_purchases*product_top_sims)/sum(product_top_sims))
            # wait = input("PRESS ENTER TO CONTINUE.")
            data_sims.iloc[i][j] = getScore(user_purchases,product_top_sims)

# Get the top songs
data_recommend = pd.DataFrame(index=data_sims.index, columns=range(1,6))

# Instead of top song scores, we want to see names

for i in range(0,len(data_sims.index)):
    data_recommend.ix[i,0:]=data_sims.iloc[i,:].order(ascending=False).iloc[0:5,].index.transpose()

print (data_recommend.iloc[:10,:4])