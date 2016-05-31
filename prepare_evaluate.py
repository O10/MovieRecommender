import pandas as pd

recomendations = pd.read_csv('data/data-full-finished/user_recomendations.csv', index_col=0)
movieTable = pd.read_csv('data/data-full-finished/movie_table.csv', index_col=0)

eval_data = pd.DataFrame(index=recomendations.index,columns=range(0,3))
print(movieTable.index[:5])
print(movieTable.loc['Gladiator (2000)'][2])
for i in range(0, len(recomendations.index)):
    eval_data.iloc[i][0] = recomendations.index[i]
    eval_data.iloc[i][1] = movieTable.loc[recomendations.iloc[i][0]]['MovieID']
    eval_data.iloc[i][2] = 5

eval_data.to_csv('data/data-full-finished/eval.csv', index=False,header=False)
