from utils import get_key_from_value
import pandas as pd


def game_data_pp_1(df):
    # df: Dataframe to process (MADE FOR game_data)

    ### This function returns the df with added columns:
    ### Abbreviation, Season and date in datetime format
    df = df[df['opp'].notnull()]

    teams = []
    years = []
    for link in df['link']:
        i = link.find('teams')
        team = link[i+6 : i+9]
        teams.append(team)

        j = link.find('20')
        year = link[j : j+4]
        years.append(year)

    df.insert(5, 'Abbreviation', [team.upper() for team in teams])
    df.insert(2, 'Season', years)

    del teams, year

    date = []
    for _, row in df[['Season', 'date']].iterrows():
        if type(row['date']) == str:
            date.append(f'{row["Season"]} {str(row["date"])}')
        else:
            date.append(row['Season'])

    df['date'] = date
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

    del date

    return df


def game_data_pp_2(df, teams):

    fn_team = []
    for abb in df['Abbreviation']:
        fn_team.append(teams[abb])

    df.insert(6, 'Team Name', fn_team)

    abbs = []
    for name in df['opp']:
        value = get_key_from_value(teams, name)
        if not value:
            abbs.append(pd.NA)
        else:
            abbs.append(value)

    df.insert(9, 'Opposing abbreviation', abbs)

    del fn_team, abbs

    df_new_columns = ['Link', 'Week', 'Season', 'Date', 'Overtime', 'Record', 'Team', 'Abbreviation', 'Opposing team', 'Opposing abbreviation', 'Score', 'Opposing score', 'Firstdowns gained', 'Total yards gained', 'Pass yards gained', 'Rush yards gained', 'Offensive turnovers', 'Firstdowns allowed', 'Total yards allowed', 'Pass yards allowed', 'Rush yards allowed', 'Defensive turnovers', 'Expected points (offense)', 'Expected points (defense)', 'Expected points (special team)']
    df.columns = df_new_columns

    df_ordered_columns = ['Date', 'Season', 'Week', 'Team', 'Abbreviation', 'Opposing team', 'Opposing abbreviation', 'Score', 'Opposing score', 'Overtime', 'Record', 'Firstdowns gained', 'Total yards gained', 'Pass yards gained', 'Rush yards gained', 'Offensive turnovers', 'Firstdowns allowed', 'Total yards allowed', 'Pass yards allowed', 'Rush yards allowed', 'Defensive turnovers', 'Expected points (offense)', 'Expected points (defense)', 'Expected points (special team)', 'Link']
    df = df[df_ordered_columns]

    del df_new_columns, df_ordered_columns

    return df


def game_data_pp_3(df):
    home1 = []
    home2 = []
    away1 = []
    away2 = []
    cols = ['Away?', 'Team', 'Abbreviation', 'Opposing team', 'Opposing abbreviation']

    for _, row in df[cols].iterrows():
        if row['Away?'] == '@':
            home1.append(row['Opposing team'])
            away1.append(row['Team'])
            home2.append(row['Opposing abbreviation'])
            away2.append(row['Abbreviation'])
        else:
            home1.append(row['Team'])
            away1.append(row['Opposing team'])
            home2.append(row['Abbreviation'])
            away2.append(row['Opposing abbreviation'])
    
    df = df.drop(cols, axis=1)

    df.insert(3, 'Home Team', home1)
    df.insert(4, 'Abbreviation (home)', home2)
    df.insert(5, 'Away Team', away1)
    df.insert(6, 'Abbreviation (away)', away2)

    del home1, home2, away1, away2, cols

    return df



def nfl_elo_pp_1(df, sub_num=0):
    # df: Dataframe to process (MADE FOR nlf_elo)
    # sub_num: factor for how many "samples" per team for the df subset

    ### This function returns the cleaned (from NaN rows) df with date column in datetime format,
    ### a list of teams with abbreviations waiting for full names to add,
    ### and, if sub_num>0, a subset of the df scaled with sub_num
    ### (bigger sub_num increases the chances of getting a total match for each abbreviation)

    df['date'] = pd.to_datetime(df['date'], format="%Y/%m/%d")

    teams2add = []
    df = df[df['team1'].notnull() | df['team2'].notnull()]

    for _, row in df[['team1', 'team2']].iterrows():
        team1 = row['team1']
        team2 = row['team2']

        if team1 not in teams2add:
            teams2add.append(team1)
        if team2 not in teams2add:
            teams2add.append(team2)

    teams2add = set(sorted(teams2add))

    if sub_num > 0:
        df_sub = pd.DataFrame()

        for i in teams2add:
            temp1 = df[df['team1'] == i][: sub_num]
            temp2 = df[df['team2'] == i][: sub_num]

            if (temp1.shape[0] or temp2.shape[0]) == 0:
                temp = df[(df['team1'] == i) | (df['team2'] == i)][: 2*sub_num]
            else:
                temp = pd.concat([temp1, temp2])

            df_sub = pd.concat([df_sub, temp])

    return df, teams2add, df_sub


def nfl_elo_pp_2(df, teams):

    t1 = []
    t2 = []
    for _, row in df[['team1', 'team2']].iterrows():
        if row['team1'] in teams:
            value1 = teams[row['team1']]
        else:
            value1 = None

        if row['team2'] in teams:
            value2 = teams[row['team2']]
        else:
            value2 = pd.NA

        t1.append(value1)
        t2.append(value2)

    df.insert(4, 'Home Team', t1)
    df.insert(6, 'Away Team', t2)

    del t1, t2

    return df



def nfl_pp(df, teams):

    ht = []
    at = []
    for _, row in df[['Home Team', 'Away Team']].iterrows():

        hometeam = row['Home Team']
        value1 = get_key_from_value(teams, hometeam)
        if not hometeam:
            ht.append(None)
        else:
            ht.append(value1)
        
        awayteam = row['Away Team']
        value2 = get_key_from_value(teams, awayteam)
        if not value2:
            at.append(None)
        else:
            at.append(value2)
        
    df.insert(2, 'Home Abbreviation', ht)
    df.insert(4, 'Away Abbreviation', at)

    del ht, at

    return df



