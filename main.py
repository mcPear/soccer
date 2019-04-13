import pandas as pd
import sqlite3

database = 'database.sqlite'
conn = sqlite3.connect(database)

features = pd.read_sql("""SELECT B365H, B365D, B365A, CASE
     WHEN home_team_goal - away_team_goal>0 THEN 1
     WHEN home_team_goal - away_team_goal<0 THEN -1
     WHEN home_team_goal - away_team_goal==0 THEN 0 END home_won
     FROM Match WHERE B365H IS NOT NULL;""", conn)


def get_wins_perc(s):
    n = 1 / (100 * s / 100 - 1)
    return n * 100 / (n + 1)


def get_wins_ratio(h, d, a):
    return [get_wins_perc(h), get_wins_perc(d), get_wins_perc(a)]


def get_wins_pred(features, h, d, a, e):
    h_about = ((h - e) <= features['B365H']) & (features['B365H'] <= (h + e))
    d_about = ((d - e) <= features['B365D']) & (features['B365D'] <= (d + e))
    a_about = ((a - e) <= features['B365A']) & (features['B365A'] <= (a + e))

    features = features[h_about]
    features = features[d_about]
    features = features[a_about]

    count = features.iloc[:, 1].count()
    if not count:
        return []
    home_wins = features[features['home_won'] == 1].iloc[:, 1].count()
    draws = features[features['home_won'] == 0].iloc[:, 1].count()
    away_wins = features[features['home_won'] == -1].iloc[:, 1].count()

    return [home_wins * 100 / count, draws * 100 / count, away_wins * 100 / count]


def analyse(h, d, a, e, features):
    wins_pred = get_wins_pred(features, h, d, a, e)

    print(
        f"{round(h - e, 2)} - {round(h + e, 2)} | {round(d - e, 2)} - {round(d + e, 2)} | {round(a - e, 2)} - "
        f"{round(a + e, 2)}")

    if wins_pred:
        wins_ratio = f"req: {[round(x, 2) for x in get_wins_ratio(h, d, a)]}"
        wins_pred_str = f"pred: {[round(x, 2) for x in wins_pred]}"

        print(wins_ratio)
        print(wins_pred_str)
    else:
        print("Cannot fount similar matches")
    print("-")


def find_positive_configurations():
    h, d, a, e, step = [1.0, 3.0, 1.0, 0.07, 0.1]
    for hi in range(20):
        for di in range(20):
            for ai in range(20):
                analyse(h + step * hi, d + e * di, a + step * ai, e, features)


matches = pd.read_csv('italy.csv', sep='\t')
print(matches)
for index, row in matches.iterrows():
    analyse(row[2], row[3], row[4], 0.7, features)

# fixme maybe it would be better to ignore draws, it is less correlated but constraints harder
# todo include country, league, season...

# print(features)
