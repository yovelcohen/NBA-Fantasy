from json import load
import pandas as pd
import urllib
import datetime

pd.set_option('display.max_columns', 20)


# ask fatty why pychram suggested to move this method outside the class.
def flatten(l):
    return [item for sublist in l for item in sublist]


class AthletesJsonReader(object):
    def __init__(self, df=None, names=None, player_name=None, end_name=None,
                 fgm=None, fga=None, fgp=None,
                 three_pm=None, three_attempted=None, three_percent=None,
                 ftm=None, fta=None, percent_ft=None,
                 pts=None, ast=None, stl=None, blk=None,reb=None,
                 player_stats=None):
        if blk is None:
            blk = []
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
        if three_pm is None:
            three_pm = []
        if fgp is None:
            fgp = []
        if fga is None:
            fga = []
        if fgm is None:
            fgm = []
        if reb is None:
            reb = []
        if pts is None:
            pts = []
        if names is None:
            names = []

        url = urllib.request.urlopen(
            'http://site.api.espn.com/apis/common/v3/sports/basketball/nba/statistics/byathlete?contentorigin=espn'
            '&isqualified=true&lang=en&region=us&sort=offensive.avgPoints%3Adesc&limit=400')
        self.json_data = load(url)
        self.df = df
        self.player_stats = player_stats
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
        self.player_name = player_name
        self.end_name = end_name

    def get_names(self):
        first = []
        # get player's names in to a list and on to the csv file.
        for athlete in self.json_data['athletes']:
            first.append([athlete['athlete']['displayName']])
            self.names = flatten(first)

    # index :
    # 0 -stl  , 1 - blk

    def get_blk_stl(self):
        for row in self.json_data['athletes']:
            stl_blk = (list(row['categories'][2]['totals'][0:2]))
            self.stl.append(stl_blk[0])
            self.stl = list(map(float, self.stl))
            self.blk.append(stl_blk[1])
            self.blk = list(map(float, self.blk))

    #  0   1   2    3   4   5   6   7   8   9   10
    # pts fgm fga fg% 3pm 3pa  3p%  ftm fta ft% ast

    def get_most_stats(self):
        for row in self.json_data['athletes']:
            most_stats = row['categories'][1]['totals'][0:11]
            self.pts.append(most_stats[0])
            self.pts = list(map(float, self.pts))
            self.fgm.append(most_stats[1])
            self.fgm = list(map(float, self.fgm))
            self.fga.append(most_stats[2])
            self.fga = list(map(float, self.fga))
            self.fgp.append(most_stats[3])
            self.fgp = list(map(float, self.fgp))
            self.three_pm.append(most_stats[4])
            self.three_pm = list(map(float, self.three_pm))
            self.three_attempted.append(most_stats[5])
            self.three_attempted = list(map(float, self.three_attempted))
            self.three_percent.append(most_stats[6])
            self.three_percent = list(map(float, self.three_percent))
            self.ftm.append(most_stats[7])
            self.ftm = list(map(float, self.ftm))
            self.fta.append(most_stats[8])
            self.fta = list(map(float, self.fta))
            self.percent_ft.append(most_stats[9])
            self.percent_ft = list(map(float, self.percent_ft))
            self.ast.append(most_stats[10])
            self.ast = list(map(float, self.ast))

    # only the last index.
    def get_rebs(self):
        for row in self.json_data['athletes']:
            self.reb.append(row['categories'][0]['totals'][-1])
            self.reb = list(map(float, self.reb))

    def pd_table(self):
        d = {'Name': self.names, 'PTS': self.pts, 'REB': self.reb, 'AST': self.ast, 'STL': self.stl,
             'BLK': self.blk, 'FGM': self.fgm, 'FGA': self.fga, 'FG%': self.fgp, '3PM': self.three_pm,
             '3PA': self.three_attempted, '3P%': self.three_percent, 'FTM': self.ftm,
             'FTA': self.fta, 'FT%': self.percent_ft}
        self.df = pd.DataFrame(d)
        self.df.index.name = 'updated to: ', pd.Timestamp(
            datetime.datetime.now().replace(second=0, microsecond=0))
        print(self.df)

    def sum_players_stats(self):
        player_1 = self.get_player_stats()
        player_2 = self.get_player_stats()
        df_player1 = pd.DataFrame(player_1)
        df_player2 = pd.DataFrame(player_2)
        fin_df = df_player1.append(df_player2, ignore_index=True)
        pts = round(fin_df['PTS'][0] - fin_df['PTS'][1], 1)
        reb = round(fin_df['REB'][0] - fin_df['REB'][1], 1)
        ast = round(fin_df['AST'][0] - fin_df['AST'][1], 1)
        threes = round(fin_df['3PM'][0] - fin_df['3PM'][1], )
        fg = (fin_df['FG%'][0] + fin_df['FG%'][1]) / 2
        stl = round(fin_df['STL'][0] - fin_df['STL'][1], 1)
        blk = round(fin_df['BLK'][0] - fin_df['BLK'][1], 1)
        print('The PPG difference between {} '.format(player_1['Name'][0]) + 'and {} is: {} '.format(
            self.end_name, pts))
        print('The RPG difference between {} '.format(player_1['Name'][0]) +
              'and {} is: {} '.format(self.end_name, reb))
        print('The APG difference between {} '.format(player_1['Name'][0]) +
              'and {} is: {} '.format(self.end_name, ast))
        print('the average FG % of the two players is {}'.format(fg))
        print('The 3PM difference between {} '.format(player_1['Name'][0]) +
              'and {} is: {} '.format(self.end_name, threes))
        print('The STL difference between {} '.format(player_1['Name'][0]) +
              'and {} is: {} '.format(self.end_name, stl))
        print('The BLK difference between {} '.format(player_1['Name'][0]) +
              'and {} is: {} '.format(self.end_name, blk))


parser = AthletesJsonReader()
parser.get_names()
parser.get_blk_stl()
parser.get_most_stats()
parser.get_rebs()
parser.pd_table()
