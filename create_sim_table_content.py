import pandas as pd
from scipy.spatial.distance import cosine

testdata='data/test.csv'
actualdata='data/recsysrules-train.csv'

data = pd.read_csv(testdata)
uniqueMovies = pd.unique(data.get("Title"))

print("Creating Movie Table")

movieTable=pd.DataFrame(index=uniqueMovies,columns=data.columns)

for i in range(0,len(movieTable.index)):
    currentMovie=movieTable.index[i]
    currentMovieData=data[data['Title']==currentMovie].iloc[0][:]
    movieTable.iloc[i][:]=currentMovieData

movieTable.drop(movieTable.columns[0:19],axis=1,inplace=True)
print(movieTable.iloc[0][0:20])
wait = input("PRESS ENTER TO CONTINUE.")
print("Done")

print("Calculating simillarities")
simillarityMatrix = pd.DataFrame(index=movieTable.index,columns=movieTable.index)

for i in range(0,len(simillarityMatrix.columns)) :
    for j in range(0,len(simillarityMatrix.columns)) :
      simillarityMatrix.iloc[i,j] = 1-cosine(movieTable.iloc[i,:],movieTable.iloc[j,:])

print("Done")

print("Finding and printing best matches")

dataNeighbours = pd.DataFrame(index=simillarityMatrix.columns, columns=range(1, 11))

for i in range(0,len(simillarityMatrix.columns)):
    dataNeighbours.iloc[i, :10] = simillarityMatrix.iloc[:, i].order(ascending=False)[0:10].index

dataNeighbours.to_csv('data/sim_table_content.csv')
simillarityMatrix.to_csv('data/sim_matrix_content.csv')
print("Done")
