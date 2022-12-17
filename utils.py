from random import choice
from duckduckgo_search import ddg
import pickle


def get_key_from_value(dic, val):
    for key, value in dic.items():
        if val == value:
            return key


def random_proxy(proxy_path = 'proxies.txt'):

    with open(proxy_path, 'r') as reader:
        proxy_list = [line.rstrip() for line in reader]

    proxy = {'https': f'https://{choice(proxy_list)}'}
    return proxy



def to_pickle(object, pickle_path):

    with open(pickle_path, 'wb') as p: # Dumping to TEAMS.pkl file
        pickle.dump(object, p)


def from_pickle(pickle_path):

    with open(pickle_path, 'rb') as p:
        object = pickle.load(p)

    return object
    


def search_teams_1(season, team_i, teams):
    # season: season of the game
    # team_i: team abbreviation
    # teams: prexisting or initiated dict

    ### MADE FOR nfl_elo

    keywords = f'{season} {team_i}'
    results = ddg(keywords, safesearch='off', region='us-en')

    for result in results:
        url = result['href']

        if ('pro-football-reference') in url and (f'teams/{team_i.lower()}') in url:
            title = result['title']
            print(title)
            print(url)
        
            team = title.split(' Roster', 1)[0]
            
            ### TO CATCH ONE MISTAKE:
            if 'Single-Season' in team:
                team = team.split(' Single-Season', 1)[0]
            else:
                team = team[4::]
            

            teams[team_i] = team
            print(f'{team_i}: {team}')
            print('------')
            break


def search_teams_2(date, team1_i, team2_i, teams):
    # data: date of the game
    # team1_i: team1 abbreviation
    # team2_i: team2 abbreviation
    # teams: prexisting or initiated dict

    ### MADE FOR nfl_elo

    keywords = f'{date} {team1_i} {team2_i}'
    results = ddg(keywords, safesearch='off', region='us-en')

    for result in results:
        url = result['href']

        if ('pro-football-reference') in url and ('boxscores') in url:
            title = result['title']
            print(title)
            print(url)
        
            team2, team1 = title.split(' at', 1)
            team1 = team1.split(' -', 1)[0]

            if team1_i not in teams:
                teams[team1_i] = team1
                print(f'{team1_i}: {team1}')

            if team2_i not in teams:
                teams[team2_i] = team2
                print(f'{team2_i}: {team2}')

            print('------')
            break