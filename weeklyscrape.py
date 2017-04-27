import urllib2
import scraper
import re

if __name__ == "__main__":    
    response = urllib2.urlopen("http://pgatour.com/leaderboard.html")
    source = response.read()
    
    #A couple regexs to find the tournament id and year from html source.
    tournament_id = re.search(r"tournamentId: '(\d{3})'", source).group(1)
    year = re.search(r"year: '(\d{4})'", source).group(1)
    
    scraper.scrape(tournament_id, year)
    