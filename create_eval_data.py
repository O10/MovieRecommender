import pandas as pd
import sys

datafile = 'data/recsysrules-train.csv'
# datafile = 'data/test.csv'

if len(sys.argv) > 1:
    datafile = sys.argv[1]

data = pd.read_csv(datafile, index_col=0)
usersDone = set()                   # A new empty set

train_index=[]
test_index=[]

for i in range(0,len(data.index)):
    currentRow=data.iloc[i][:]
    currentUser=currentRow.loc['UserID']
    movieScore=currentRow.loc['Rating']
    if(not(currentUser in usersDone) and movieScore >=5 ):
        test_index.append(i)
        usersDone.add(currentUser)
    else:
        train_index.append(i)

data_train=data.iloc[train_index][:]
data_test=data.iloc[test_index][:]

data_train.to_csv("data/data_train.csv")
data_test.to_csv("data/data_test.csv")