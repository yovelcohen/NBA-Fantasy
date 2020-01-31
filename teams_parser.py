from bs4 import BeautifulSoup
import urllib.request as urllib

url = urllib.urlopen('https://fantasy.espn.com/basketball/league/rosters?leagueId=49098385')
soup = BeautifulSoup(url, 'html.parser')
names = soup.prettify()
print(names)