import datetime
import json
import urllib
import pandas as pd
from consts import CATEGORIES, ATHLETES, TOTALS, LEN_STATS, index
from utils import flatten

pd.set_option('display.max_columns', 20)
pd.set_option("display.precision", 3)


class AthletesJsonReader(object):

    def __init__(self, df=None, player_stats=None, end_name=None, player_name=None, names=None, stats_list=None,
                 fgm=None, fga=None, fgp=None,
                 three_pm=None, three_attempted=None,
                 ftm=None, fta=None, percent_ft=None,
                 pts=None, ast=None, three_percent=None, stl=None,
                 blk=None, reb=None, ):
        if three_pm is None:
            three_pm = []
        if names is None:
            names = []
        if stats_list is None:
            stats_list = []
        if fgm is None:
            fgm = []
        if pts is None:
            pts = []
        if reb is None:
            reb = []
        if fga is None:
            fga = []
        if fgp is None:
            fgp = []
        if stl is None:
            stl = []
        if three_percent is None:
            three_percent = []
        if ast is None:
            ast = []
        if percent_ft is None:
            percent_ft = []
        if fta is None:
            fta = []
        if ftm is None:
            ftm = []
        if three_attempted is None:
            three_attempted = []
        if blk is None:
            blk = []
        attributes_list = [df, names, stats_list, fgm, pts, reb, fga, fgp, three_attempted, three_percent, three_pm,
                           ftm, fta, percent_ft, ast, stl, blk]

        url = urllib.request.urlopen(
            'http://site.api.espn.com/apis/common/v3/sports/basketball/nba/statistics/byathlete?contentorigin=espn'
            '&isqualified=true&lang=en&region=us&sort=offensive.avgPoints%3Adesc&limit=400')
        self.json_data = json.load(url)
        self.df = df
        self.names = names
        self.fgm = fgm
        self.reb = reb
        self.pts = pts
        self.fga = fga
        self.fgp = fgp
        self.fta = fta
        self.ftm = ftm
        self.three_attempted = three_attempted
        self.three_pm = three_pm
        self.percent_ft = percent_ft
        self.ast = ast
        self.three_percent = three_percent
        self.stl = stl
        self.blk = blk
        self.stats_list = stats_list
        self.player_stats = player_stats
        self.end_name = end_name
        self.player_name = player_name

    def get_names(self):
        first = []
        # get player's names in to a list and on to the csv file.
        for athlete in self.json_data[ATHLETES]:
            first.append([athlete['athlete']['displayName']])
            self.names = flatten(first)

    def get_blk_stl(self):
        for row in self.json_data[ATHLETES]:
            stl_blk = (list(row['categories'][2]['totals'][0:2]))
            self.stl.append(stl_blk[0])
            self.stl = list(map(float, self.stl))
            self.blk.append(stl_blk[1])
            self.blk = list(map(float, self.blk))

    def get_most_stats(self, index=index):
        for row in self.json_data[ATHLETES]:
            most_stats = row[CATEGORIES][1][TOTALS][0:11]
            self.stats_list = [self.pts, self.fgm, self.fga, self.fgp, self.three_pm, self.three_attempted,
                               self.three_percent, self.ftm, self.fta, self.percent_ft, self.ast]
            while index < LEN_STATS:
                float_stat = float(most_stats[index])
                self.stats_list[index].append(float_stat)
                index += 1

    # only the last index.
    def get_rebs(self):
        for row in self.json_data[ATHLETES]:
            self.reb.append(float(row['categories'][0]['totals'][-1]))

    def pd_table(self):
        d = {'Name': self.names,
             'PTS': self.pts, 'REB': self.reb, 'AST': self.ast, 'STL': self.stl, 'BLK': self.blk,
             'FGM': self.fgm, 'FGA': self.fga, 'FG%': self.fgp,
             '3PM': self.three_pm, '3PA': self.three_attempted, '3P%': self.three_percent,
             'FTM': self.ftm, 'FTA': self.fta, 'FT%': self.percent_ft
             }
        self.df = pd.DataFrame(d)
        self.df.index.name = 'updated to: ', pd.Timestamp(
            datetime.datetime.now().replace(second=0, microsecond=0))
        return self.df

    def to_csv(self):
        return self.df.to_csv('csv_stats.csv')

# print(time.clock())
