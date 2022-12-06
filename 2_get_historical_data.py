from bs4 import BeautifulSoup
import requests
import pandas as pd

years = [2010, 2014, 2018, 2022]


def get_historic_matches(year):
    web_url = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    response = requests.get(web_url)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')

    matches = soup.find_all('div', class_='footballbox')

    team1 = []
    team2 = []
    goals = []
    goalsErhalten = []

    for match in matches:
        # use this to already include historic matches of the current cup
        if match.find('th', class_='fscore').get_text().strip().startswith('Match'):
            continue
        score_dirty = match.find('th', class_='fscore').get_text().replace('(a.e.t.)', '')
        score = score_dirty.strip()
        goals.append(score.split('–')[0])
        goalsErhalten.append(score.split('–')[1])
        team1.append(match.find('th', class_='fhome').get_text().strip())
        team2.append(match.find('th', class_='faway').get_text().strip())

    dict_matches = {'team1': team1, 'goals': goals, 'goalsGotten': goalsErhalten, 'team2': team2}
    df_matches = pd.DataFrame(dict_matches)
    df_matches['year'] = f'{year}'
    return df_matches


def get_current_fixture(year):
    url = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')

    matches = soup.find_all('div', class_='footballbox')

    team1 = []
    team2 = []
    score = []

    for match in matches:
        # use this to already include historic matches of the current cup
        if not match.find('th', class_='fscore').get_text().strip().startswith('Match'):
            continue
        team1.append(match.find('th', class_='fhome').get_text().strip())
        score.append(match.find('th', class_='fscore').get_text().strip())
        team2.append(match.find('th', class_='faway').get_text().strip())

    dict_matches = {'team1': team1, 'score': score, 'team2': team2}
    df_matches = pd.DataFrame(dict_matches)
    df_matches['year'] = f'{year}'
    return df_matches



historic_matches = [get_historic_matches(year) for year in years]
df_historic_matches = pd.concat(historic_matches, ignore_index=True)
df_historic_matches.to_csv('./historic_matches.csv', index=False)


# get fixture data for the current cup
df_fixture = get_current_fixture('2022')
df_fixture.to_csv('./current_cup_fixture.csv', index=False)
