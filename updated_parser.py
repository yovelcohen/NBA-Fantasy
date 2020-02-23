import datetime
import json
import urllib
from pprint import pprint

import pandas as pd
from consts import CATEGORIES, ATHLETES, TOTALS, LEN_STATS, INDEX
from utils import flatten

pd.set_option('display.max_columns', 20)
pd.set_option("display.precision", 3)


class AthletesJsonReader(object):

    def __init__(self):

        url = urllib.request.urlopen(
            'http://site.api.espn.com/apis/common/v3/sports/basketball/nba/statistics/byathlete?contentorigin=espn'
            '&isqualified=true&lang=en&region=us&sort=offensive.avgPoints%3Adesc&limit=400')

        self.json_data = json.load(url)

    def get_names(self):
        first = []
        # get player's names in to a list and on to the csv file.
        for athlete in self.json_data[ATHLETES]:
            first.append([athlete['athlete']['displayName']])
            names = flatten(first)
            return names

    def get_stats(self, INDEX=INDEX):

        stats_list = [pts, fgm, fga, fgp, three_pm, three_attempted,
                      three_percent, ftm, fta, percent_ft, ast]



        most_stats = [row[CATEGORIES][1][TOTALS][0:11] for row in self.json_data[ATHLETES]]
        while INDEX < LEN_STATS:
            stats_list[INDEX] = [l[INDEX] for l in most_stats]
            INDEX += 1

        # steals and blocks.
        for row in self.json_data[ATHLETES]:
            stl_blk = list(row['categories'][2]['totals'][0:2])
        # rebounds
        reb = [float(row[CATEGORIES][0][TOTALS][-1]) for row in self.json_data[ATHLETES]]
        pprint(reb)
        return reb, stats_list

    def pd_table(self):
        d = {'Name': names,
             'PTS': pts, 'REB': reb, 'AST': ast, 'STL': stl, 'BLK': blk,
             'FGM': fgm, 'FGA': fga, 'FG%': fgp,
             '3PM': three_pm, '3PA': three_attempted, '3P%': three_percent,
             'FTM': ftm, 'FTA': fta, 'FT%': percent_ft
             }
        stats_list = [self.pts, self.fgm, self.fga, self.fgp, self.three_pm, self.three_attempted,
                      self.three_percent, self.ftm, self.fta, self.percent_ft, self.ast, self.blk, self.stl, self.reb]

        for item in stats_list:
            print(len(item))

        self.df = pd.DataFrame(d)
        self.df.index.name = 'updated to: ', pd.Timestamp(
            datetime.datetime.now().replace(second=0, microsecond=0))
        return self.df

    def to_csv(self):
        return self.df.to_csv('csv_stats.csv')


a = AthletesJsonReader()
a.get_names()
a.get_blk_stl()
a.get_most_stats()
a.get_rebs()
