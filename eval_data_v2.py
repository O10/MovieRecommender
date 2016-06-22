import pandas as pd
import math

numRecom = 10

userScores = pd.read_csv('data/user_rec_score.csv', index_col=0)
testData = pd.read_csv('data/rating_table_test.csv', index_col=0)
movietable = pd.read_csv('data/movie_table.csv', index_col=0)

evalFrame = pd.DataFrame(index=testData.index, columns=['Precision', 'Recall'])

hitsum = 0
recallsum = 0

for i in range(0, len(testData.index)):
    currentUID = testData.index[i]
    currentTopScores = userScores.loc[currentUID].order(ascending=False)[0:numRecom]
    currentTestScores = testData.loc[currentUID][testData.loc[currentUID] == 5]
    currentTestIndex = currentTestScores.index
    try:
        t = currentTopScores.loc[currentTestIndex]
        t.dropna(inplace=True)
    except:
        t = []
    hits = len(t)
    evalFrame.iloc[i].loc["Precision"] = str(hits) + "/" + str(numRecom)
    evalFrame.iloc[i].loc["Recall"] = str(hits) + "/" + str(len(currentTestScores))
    hitsum += hits
    recallsum += len(currentTestScores)

print("Average Precision", math.ceil(hitsum / len(testData.index)), "/", numRecom)
print("Average Recall", math.ceil(hitsum / len(testData.index)), "/", int(recallsum / len(testData.index)))

evalFrame.to_csv("data/eval_frame.csv")
