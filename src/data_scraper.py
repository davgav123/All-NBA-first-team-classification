#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

# from 1979-1980 to 2018-2019 season, 3-point era
three_point_era_seasons = [season for season in range(1980, 2020)]

per_game_url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'
totals_url = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'
per_36_url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_minute.html'
per_100_poss_url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_poss.html'
advanced_url = 'https://www.basketball-reference.com/leagues/NBA_{}_advanced.html'

all_nba_centers = [
    (2019, 'Nikola Jokić'),
    (2018, 'Anthony Davis'),
    (2017, 'Anthony Davis'),
    (2016, 'DeAndre Jordan'),
    (2015, 'Marc Gasol'),
    (2014, 'Joakim Noah'),
    (2013, 'Tim Duncan'),
    (2012, 'Dwight Howard'),
    (2011, 'Dwight Howard'),
    (2010, 'Dwight Howard'),
    (2009, 'Dwight Howard'),
    (2008, 'Dwight Howard'),
    (2007, "Amar'e Stoudemire"),
    (2006, "Shaquille O'Neal"),
    (2005, "Shaquille O'Neal"),
    (2004, "Shaquille O'Neal"),
    (2003, "Shaquille O'Neal"),
    (2002, "Shaquille O'Neal"),
    (2001, "Shaquille O'Neal"),
    (2000, "Shaquille O'Neal"),
    (1999, 'Alonzo Mourning'),
    (1998, "Shaquille O'Neal"),
    (1997, 'Hakeem Olajuwon'),
    (1996, 'David Robinson'),
    (1995, 'David Robinson'),
    (1994, 'Hakeem Olajuwon'),
    (1993, 'Hakeem Olajuwon'),
    (1992, 'David Robinson'),
    (1991, 'David Robinson'),
    (1990, 'Patrick Ewing'),
    (1989, 'Hakeem Olajuwon'),
    (1988, 'Hakeem Olajuwon'),
    (1987, 'Hakeem Olajuwon'),
    (1986, 'Kareem Abdul-Jabbar'),
    (1985, 'Moses Malone'),
    (1984, 'Kareem Abdul-Jabbar'),
    (1983, 'Moses Malone'),
    (1982, 'Moses Malone'),
    (1981, 'Kareem Abdul-Jabbar'),
    (1980, 'Kareem Abdul-Jabbar')
]

# This code is a modification of the code that can be found on: 
# https://towardsdatascience.com/web-scraping-nba-stats-4b4f8c525994
def scrap_bbref_table(year, target_table_url):
    url = target_table_url.format(year)
    
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    # get headers
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    headers = headers[1:]

    # rest of the data
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]

    stats = pd.DataFrame(player_stats, columns=headers)
    
    # delete empty rows, rows where 'Player' field is missing
    # those rows are missing because of html
    stats = stats[pd.notnull(stats['Player'])]
    stats = stats.reset_index(drop=True)

    print('Reading data from {} finished'.format(url))
    return stats


def data_from_url(url, dest_path, seasons):
    dest_df = pd.DataFrame()

    for season in seasons:
        df = scrap_bbref_table(season, url)

        # take centers
        df = df[df.Pos.isin(['C', 'C-PF', 'PF-C', 'PF'])]

        # add season colum
        df['season'] = season
        df['all_nba_1st_team'] = 0

        # take (season, player) pair from the list, and update dataframe
        all_nba_1st_team_center = list(filter(lambda x: x[0] == season, all_nba_centers))[0][1]

        # '*' sign marks hall of famers
        valid_names = [all_nba_1st_team_center, all_nba_1st_team_center + '*']
        df.loc[df['Player'].isin(valid_names), 'all_nba_1st_team'] = 1
        df.loc[~df['Player'].isin(valid_names), 'all_nba_1st_team'] = 0

        dest_df = pd.concat([dest_df, df], ignore_index=True)

    dest_df.to_csv(dest_path, index=False)
    print('Data is saved into {}'.format(dest_path))


if __name__ == "__main__":
    data_from_url(per_game_url, Path('../data/per_game_data.csv'), three_point_era_seasons)
    data_from_url(totals_url, Path('../data/totals_data.csv'), three_point_era_seasons)
    data_from_url(per_36_url, Path('../data/per_36_data.csv'), three_point_era_seasons)
    data_from_url(per_100_poss_url, Path('../data/per_100_data.csv'), three_point_era_seasons)
    data_from_url(advanced_url, Path('../data/advanced_data.csv'), three_point_era_seasons)    
