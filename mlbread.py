import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://www.espn.com/mlb/scoreboard/_/date/20230818'

# Send a GET request and retrieve HTML content
response = requests.get(url)
html_content = response.text

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Example: Extract team names and scores from the webpage
game_rows = soup.find_all('div', class_='scoreboard game-center align-items-center')
for row in game_rows:
    team_names = row.find_all('span', class_='sb-team-short')
    team_scores = row.find_all('div', class_='total')
    if len(team_names) == 2 and len(team_scores) == 2:
        home_team_name = team_names[0].text
        away_team_name = team_names[1].text
        home_team_score = team_scores[0].text
        away_team_score = team_scores[1].text
        print(f"{home_team_name} {home_team_score} - {away_team_score} {away_team_name}")
