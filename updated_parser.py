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

    def get_names(self, INDEX=INDEX):
        names = []
        players = len(self.json_data[ATHLETES])
        while INDEX < players:
            names.append(self.json_data[ATHLETES][INDEX]['athlete']['displayName'])
            INDEX += 1
        return names

    def get_stats(self, INDEX=INDEX):
        stats_list = []

        most_stats = [row[CATEGORIES][1][TOTALS][0:11] for row in self.json_data[ATHLETES]]
        while INDEX < LEN_STATS:
            stats_list.append([l[INDEX] for l in most_stats])
            INDEX += 1

        # steals and blocks.
        stl = [float(row[CATEGORIES][0][TOTALS][0]) for row in self.json_data[ATHLETES]]
        blk = [float(row[CATEGORIES][0][TOTALS][1]) for row in self.json_data[ATHLETES]]

        # rebounds
        reb = [float(row[CATEGORIES][0][TOTALS][-1]) for row in self.json_data[ATHLETES]]

        return reb, blk, stl, stats_list

    def pd_table(self, names, stats):
        names = names
        reb, blk, stl, stats_list = stats

        d = {'Name': names,
             'PTS': stats_list[0], 'REB': reb, 'AST': stats_list[-1], 'STL': stl, 'BLK': blk,
             'FGM': stats_list[1], 'FGA': stats_list[2], 'FG%': stats_list[3],
             '3PM': stats_list[4], '3PA': stats_list[5], '3P%': stats_list[6],
             'FTM': stats_list[7], 'FTA': stats_list[8], 'FT%': stats_list[9]
             }

        df = pd.DataFrame(d)
        df.index.name = 'updated to: ', pd.Timestamp(
            datetime.datetime.now().replace(second=0, microsecond=0))

        return df

    def to_csv(self, df):
        return df.to_csv('csv_stats.csv')


a = AthletesJsonReader()
a.pd_table(names=a.get_names(), stats=a.get_stats())
