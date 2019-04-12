import pandas as pd
import sqlite3

database = 'database.sqlite'
conn = sqlite3.connect(database)

features = pd.read_sql("""SELECT B365H, B365D, B365A, CASE
     WHEN home_team_goal - away_team_goal>0 THEN 1
     WHEN home_team_goal - away_team_goal<0 THEN -1
     WHEN home_team_goal - away_team_goal==0 THEN 0 END home_won
     FROM Match WHERE B365H IS NOT NULL;""", conn)

h, d, a, e = [1.9, 3.5, 4.39, 0.07]

h_about = ((h - e) <= features['B365H']) & (features['B365H'] <= (h + e))
d_about = ((d - e) <= features['B365D']) & (features['B365D'] <= (d + e))
a_about = ((a - e) <= features['B365A']) & (features['B365A'] <= (a + e))

features = features[h_about]
features = features[d_about]
features = features[a_about]

count = features.iloc[:, 1].count()
home_wins = features[features['home_won'] == 1].iloc[:, 1].count()
draws = features[features['home_won'] == 0].iloc[:, 1].count()
away_wins = features[features['home_won'] == -1].iloc[:, 1].count()

#fixme maybe it would be better to ignore draws, it is less correlated but constraints harder
#todo include benefit equation
#todo find in loop positive combinations of features
#todo include countre, league, season...

print(features)
print(f"{round(h - e, 2)} - {round(h + e, 2)} | {round(d - e, 2)} - {round(d + e, 2)} | {round(a - e, 2)} - {round(a + e, 2)}")
print(f"{home_wins} {round(home_wins * 100 / count, 2)}%")
print(f"{draws} {round(draws * 100 / count, 2)}%")
print(f"{away_wins} {round(away_wins * 100 / count, 2)}%")
