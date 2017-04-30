# Shot Scraper
##### A PGA TOUR data scraper for personal use.

## About
Shot Scraper is a python script designed to scrape data for various PGA Tour tournaments. As of 2017, tournaments are typically located at http://pgatour.com/data/r/<tournament id\>/\<year\>/\<filename\>.json. Shot Scraper downloads various json files from these directories for analysis elsewhere. The tournament ids can be found in schedule.json located in the respective 2016/2017 folders. Additional json files can be found in the source code of http://pgatour.com/leaderboard.html, although many of them contain redudant information. 

In addition, weeklyscrape.py is a script designed to scrape the current week's tournament. This script can be easily configured to run as a scheduled task and scrape the weekly tournament after it has concluded.

## Installation
As of 4/27/2017, the python scripts are compatible with versions of python 2.7.

Furthermore, [pandas](http://pandas.pydata.org/) is used to download the json files. I opted to use it over the native json libraries because it worked better with larger json files. Thus, Pandas will need to be downloaded if it doesn't already exist. You can download pandas using pip: `pip install pandas`

On linux, weeklyscraper.py can be easily scheduled to run via [crontab](https://www.howtogeek.com/101288/how-to-schedule-tasks-on-linux-an-introduction-to-crontab-files/) after the tournament has concluded. Below is an example to run the scraper at 6:00pm on the Monday following the tournament. 

`$ crontab -e`

Then in the crontab file add the line:

`0 18 * * 1 cd /your/path/here/ && python /your/path/here/weeklyscrape.py > log.txt 2&1`

