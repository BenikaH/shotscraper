import json
import os
import pandas
import logging
import time

logging.basicConfig(level=logging.INFO, filename='downloads_log.txt', format='%(asctime)s %(message)s')

def log(message):
    logging.info(message)

def save_scorecards(tournament_id, year):
    url = "http://pgatour.com/data/r/" + tournament_id + "/" + year + "/field.json"

    players = []
    try:
        players = pandas.read_json(url)["Tournament"]["Players"]
        log("Successfully loaded players for tournament " + tournament_id)
    except:
        log("Could not download teetimes from: " + url)
        return
    
    log("Downloading scorecards...")
    for player in players:
        time.sleep(.5) #Give the server a break :)
        pid = player["TournamentPlayerId"]
        
        url = "http://pgatour.com/data/r/" + tournament_id +"/" + year + "/scorecards/" + pid + ".json"
        
        try:
            scorecard = pandas.read_json(url)
            with open(year + "/r" + tournament_id + "/scorecards/" + pid + ".json", 'w') as output:
                output.write(scorecard.to_json())
            log("Successfully downloaded scorecard for player " + pid)
        except:
            log("Could not download scorecard from: " + url)
    
def save_course(tournament_id, year):
    url = "http://pgatour.com/data/r/" + tournament_id + "/" + year + "/course.json"
    
    try:
        data = pandas.read_json(url)
        with open(year + "/r" + tournament_id + "/course.json", 'w') as output:
            output.write(data.to_json())
            
        log("Successfully saved course info for tournament " + tournament_id)
    except:
        log("Could not download course info from: " + url)
        
def save_teetimes(tournament_id, year):
    url = "http://pgatour.com/data/r/" + tournament_id + "/" + year + "/teetimes.json"
    
    try:
        data = pandas.read_json(url)
        with open(year + "/r" + tournament_id + "/teetimes.json", 'w') as output:
            output.write(data.to_json())
            
        log("Successfully save tee times for tournament " + tournament_id)
    except:
        log("Could not load teetimesfrom: " + url)
    
def save_leaderboard(tournament_id, year):
    url = "http://pgatour.com/data/r/" + tournament_id + "/" + year + "/leaderboard.json"
    
    try:
        data = pandas.read_json(url)
        
        with open(year + "/r" + tournament_id + "/leaderboard.json", 'w') as output:
            output.write(data.to_json())
            
        log("Successfully downloaded leaderboard for tournament " + tournament_id)
    except:
        log("Could not download leaderboard from: " + url)
        
def load_schedule(year):
    with open(year + '/schedule.json', 'r') as input:
        data = json.loads(input.read())
        
        return [tour["trns"] for tour in data["tours"] if tour["desc"] == "PGA TOUR"][0]       
    
def get_tournament_name(tournament_id, year):
    url = "http://pgatour.com/data/r/" + tournament_id + "/" + year + "/field.json"
    
    try:
        data = pandas.read_json(url)        
        return data["Tournament"]["TournamentName"]    
    except:
        return None
        
def scrape(tournament_id, year):    
    if not os.path.exists(year): os.makedirs(str(year))
    if not os.path.exists(year + "/r" + tournament_id): os.makedirs(year + "/r" + tournament_id)
    if not os.path.exists(year + "/r" + tournament_id + "/scorecards"): os.makedirs(year + "/r" + tournament_id + "/scorecards")
    
    log("Attemping to scrape tournament: " + tournament_id + "\tYear: " + year)
    save_leaderboard(tournament_id, year)
    save_course(tournament_id, year)
    save_teetimes(tournament_id, year)
    save_scorecards(tournament_id, year)    
        
if __name__ in "__main__":
    #This program only works for years 2016 & 2017 as of 4/26/2017. 
    year = raw_input("Enter the year: ")
    
    print "Type 'a' to download data from all tournaments for the " + year + " season."
    print "Type 's' to download data from a specific tournament for the " + year + " season."
    ans = raw_input(">").lower()
    
    if 's' in ans:
        tournament_id = raw_input("Enter the tournament id: ")
        tournament_name = get_tournament_name(tournament_id, year)
        
        if tournament_name: 
            print "Downloading data for the " + year + " " + tournament_name
            scrape(tournament_id, year)
        else:
            print "Could not find a tournament associated with tournament_id: " + tournament_id
            
    elif 'a' in ans:        
        schedule = load_schedule(year)
            
        for tournament in schedule:
            tournament_id = tournament["permNum"]
            
            scrape(tournament_id, year)


