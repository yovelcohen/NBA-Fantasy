import pandas as pd
from updated_parser import AthletesJsonReader


class PlayerStats(object):

    def __init__(self, end_name=None, player_stats=None, player_name=None):
        self.end_name = end_name
        self.player_name = player_name
        self.player_stats = player_stats
        self.df = None
        if self.df is None:
            self.df = pd.DataFrame

    def runner(self):
        pars = AthletesJsonReader()
        pars.get_blk_stl(), pars.get_most_stats(), pars.get_names(), pars.get_rebs()
        self.df = pars.pd_table()

    def get_player_stats(self):
        self.player_name = input("enter player's name: ")
        self.end_name = self.player_name.title()
        self.player_stats = pd.DataFrame(self.df.loc[self.df.Name == '{}'.format(self.end_name)])
        return self.player_stats

    def get_percentile(self):
        print(self.df.dtypes)

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


if __name__ == '__main__':
    stats = PlayerStats()
    stats.runner()
    stats.get_percentile()
