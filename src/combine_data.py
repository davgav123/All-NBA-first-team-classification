import pandas as pd
import numpy as np
from pathlib import Path


def merge_perGame_and_advanced_data():
    per_game = pd.read_csv(Path('../data/per_game_data.csv'))
    advanced = pd.read_csv(Path('../data/advanced_data.csv'))

    # print(f'per game data shape: {per_game.shape}\nadvanced data shape: {advanced.shape}')
    # print(f'per game data columns: {per_game.columns.values}\nadvanced data columns: {advanced.columns.values}')

    # drop MP from advanced data because it represents season totals, not per game
    advanced.drop(columns=['MP'], inplace=True)

    data = per_game.merge(advanced, on=['Player', 'Pos', 'Age', 'Tm', 'G', 'season', 'all_nba_1st_team'])

    # remove columns that were created while scraping the web that have only NaN values
    data.dropna(axis=1, how='all', inplace=True)

    # print(f'merged data shape: {data.shape}')
    # print(f'merged data columns: {data.columns.values}')

    return data


def merge_perPoss_and_advanced_data():
    per_poss = pd.read_csv(Path('../data/per_100_data.csv'))
    advanced = pd.read_csv(Path('../data/advanced_data.csv'))

    # print(f'per 100 poss data shape: {per_poss.shape}\nadvanced data shape: {advanced.shape}')
    # print(f'per 100 poss data columns: {per_poss.columns.values}\nadvanced data columns: {advanced.columns.values}')

    data = per_poss.merge(advanced, on=['Player', 'Pos', 'Age', 'Tm', 'G', 'MP', 'season', 'all_nba_1st_team'])
    # print(f'merged data shape: {data.shape}')
    # print(f'merged data columns: {data.columns.values}')

    # remove columns that were created while scraping the web that have only NaN values
    data.dropna(axis=1, how='all', inplace=True)

    # print(f'merged data shape: {data.shape}')
    # print(f'merged data columns: {data.columns.values}')

    # MP feature is season total. We want per game stat
    data['MP'] = np.round(data['MP'] / data['G'], 1)

    # print(f'merged data shape: {data.shape}')
    # print(f'merged data columns: {data.columns.values}')

    return data


if __name__ == "__main__":
    merge_perGame_and_advanced_data()
    merge_perPoss_and_advanced_data()
