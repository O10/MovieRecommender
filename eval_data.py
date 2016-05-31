import pandas as pd

userScores = pd.read_csv('data/user_rec_score.csv', index_col=0)
testData = pd.read_csv('data/data_test.csv', index_col=0)
movietable = pd.read_csv('data/movie_table.csv', index_col=0)

evalFrame = pd.DataFrame(index=testData.loc[:]['UserID'], columns=['testMovieScore', 'Average'])

for i in range(0, len(testData.index)):
    currentUID = testData.iloc[i].loc["UserID"]
    currentScores = userScores.loc[currentUID].sort_values(ascending=False)
    movieID = testData.iloc[i].loc['MovieID']
    movieTitle = movietable[movietable["MovieID"] == movieID].index
    evalFrame.loc[currentUID]['testMovieScore'] = currentScores.loc[movieTitle].values[0]
    evalFrame.loc[currentUID]['Average'] = currentScores[currentScores > 0].mean()

evalFrame.fillna(0, inplace=True)
evalFrameScoreTab = evalFrame[evalFrame['testMovieScore'] > 0]
totalScore = sum(evalFrameScoreTab[:]['testMovieScore'].abs() - evalFrameScoreTab[:]['Average'].abs()) / len(
    evalFrameScoreTab.index)
print("Rec score", totalScore)
evalFrameScoreTab.to_csv("data/eval_frame.csv")
