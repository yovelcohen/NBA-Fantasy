import pandas as pd
from Stats_Parser import AthletesJsonReader
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz, process

pd.set_option('display.max_columns', 20)
pd.set_option("display.precision", 3)


class PlayerStats(object):
    df = None

    @classmethod
    def runner(cls):
        pars = AthletesJsonReader()
        cls.df = pars.pd_table(names=pars.get_names(), stats=pars.get_stats())
        return cls.df

    @classmethod
    def get_player_stats(cls, player_name=input("enter player's name: ")):
        end_name = player_name.title()
        names_lists = cls.df['Name'].tolist()

        for name in names_lists:
            name_ratio = fuzz.ratio(end_name, name)
            if name_ratio > 90:
                player_stats = pd.DataFrame(cls.df.loc[cls.df.Name == '{}'.format(name)])
                print(player_stats)
                return player_stats


    @classmethod
    def get_top_scorers(cls):
        """
        This method narrows down to the 120 best scoring players in the league, calculates the averages of fieldgoal
        percentage and points per game.
        Then returns only the players that are above average in scoring and fieldgoal percentage.
        :return: A dataframe of the top scorers league filterd by fg percent and ppg.
        :rtype: pd.Dataframe
        """
        top_df = cls.df.head(n=120)
        mean_pts = top_df['PTS'].mean()
        mean_fgp = top_df['FG%'].mean()
        pts = top_df['PTS']
        fgp = top_df['FG%']
        rslt_df = top_df[
            (pts >= mean_pts) &
            (fgp >= mean_fgp)
            ]

        return rslt_df

    @classmethod
    def get_top10(cls, category):
        df = cls.df[''.format(category)].head(10)
        return df


if __name__ == '__main__':
    stats = PlayerStats()
    stats.runner()
    stats.get_player_stats()
