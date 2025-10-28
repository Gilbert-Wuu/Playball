# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup


# %%
def get_mlb():
    """
    Get MLB schedules from mlb.com
    :return: html text
    """
    # recitation: https://stackoverflow.com/questions/77129954/error-403-webscraping-project-using-beautifulsoup
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"}
    url = "https://www.mlb.com/schedule"
    response = requests.get(url, headers=headers)
    return response.content


# %%
def to_mlb_df(html):
    """
    Extract data from html and convert into pandas DataFrame
    :param html: MLB schedules html text
    :return: MLB schedules DataFrame
    """
    soup = BeautifulSoup(html, features="lxml")

    date_label = soup.find_all("div", class_="ScheduleCollectionGridstyle__DateLabel-sc-c0iua4-5 fQIzmH")
    games_containers = soup.find_all("div", {"data-mlb-test": "individualGamesContainer"})

    individual_games = []

    if games_containers and date_label:
        for idx, games_container in enumerate(games_containers):
            # Extract the corresponding game date
            game_date = date_label[idx].text.strip()

            # Find all individual game 
            game_sections = games_container.find_all("div", {"data-mlb-test": "individualGameContainerDesktop"})

            for game in game_sections:
                
                # Extract team info
                away_team = game.find(
                    "div", class_="TeamMatchupLayerstyle__AwayWrapper-sc-ouprud-1 dmSctg").find(
                    "div", class_="TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNtMxY").text.strip()

                home_team = game.find(
                    "div", class_="TeamMatchupLayerstyle__HomeWrapper-sc-ouprud-2 hHOoUi").find(
                    "div", class_="TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNtMxY").text.strip()
                
                # Extract game time
                game_time = game.find(
                    "a", class_="linkstyle__AnchorElement-sc-1rt6me7-0 lcFuuA gameinfo-gamedaylink").text.strip()

                game_info = [game_date, away_team, home_team, game_time]
                individual_games.append(game_info)

    df = pd.DataFrame(individual_games, columns=["Date", "Away", "Home", "Game"])

    return df
