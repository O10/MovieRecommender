import pandas as pd
import sys
import random

datafile = 'data/rating_table.csv'

if len(sys.argv) > 1:
    datafile = sys.argv[1]

data = pd.read_csv(datafile, index_col=0)

testDataProc = 0.25
ratingTableTrain = pd.DataFrame(index=data.index, columns=data.columns)
ratingTableTest = pd.DataFrame(index=data.index, columns=data.columns)

for i in range(0, len(data.index)):
    currentUser = data.index[i]
    userScores = data.iloc[i][:]
    userTop = userScores[userScores == 5]

    curUserDropCount = int(len(userTop) * testDataProc)
    testMoviesIndex = []
    while curUserDropCount > 0:
        rIndex = random.randrange(0, len(userTop))
        if userTop.index[rIndex] not in testMoviesIndex:
            curUserDropCount -= 1
            testMoviesIndex.append(userTop.index[rIndex])

    ratingTableTrain.iloc[i][:] = data.iloc[i][:]
    ratingTableTrain.iloc[i].loc[testMoviesIndex] = 0

    ratingTableTest.iloc[i].loc[testMoviesIndex] = 5

ratingTableTrain.to_csv("data/rating_table_train.csv")
ratingTableTest.to_csv("data/rating_table_test.csv")
