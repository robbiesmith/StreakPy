import requests
import json
from lxml import etree
import time
import datetime
import random
import user

userInfo = user.getUser()

def makePick(matchup, selection):
    try:
        s = requests.Session()
        r = s.post("https://registerdisney.go.com/jgc/v2/client/ESPN-ESPNCOM-PROD/guest/login", data = userInfo['data'], headers = {'Content-Type': 'application/json' })

        accountInfo = json.loads(r.text)

        s.cookies.update({'swid': accountInfo['data']['profile']['swid']})
        s.cookies.update({'espn_s2': accountInfo['data']['s2']})

        page = s.get('http://streak.espn.com/en/createOrUpdateEntry?matchup=m' + matchup + 'o' + selection)

    except ConnectionError:
        print("connectionerror")
        pass
    except KeyError:
        print("keyerror")
        pass


def endTime(matchup):
    format = "%m/%d/%Y %H:%M"
    start = datetime.datetime.strptime(matchup.find('DateScheduledStart').text, format)
    sport = matchup.find('Opponent').find('Sport').text
    description = matchup.find('Title').text.lower()
    if (sport == 'Soccer'):
        if "half" in description:
            return start + datetime.timedelta(hours=1)
        if "minute" in description:
            return start + datetime.timedelta(minutes=30)
        return start + datetime.timedelta(hours=2)
    elif (sport == 'NFL'):
        if "half" in description:
            return start + datetime.timedelta(minutes=90)
        if "quarter" in description:
            return start + datetime.timedelta(hours=1)
        if "qtr" in description:
            return start + datetime.timedelta(hours=1)
        if "draft" in description:
            return start + datetime.timedelta(minutes=30)
        return start + datetime.timedelta(hours=3)
    elif (sport == 'CFL'):
        if "half" in description:
            return start + datetime.timedelta(minutes=90)
        if "quarter" in description:
            return start + datetime.timedelta(hours=1)
        if "qtr" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=3)
    elif (sport == 'NCF'):
        if "half" in description:
            return start + datetime.timedelta(minutes=90)
        if "quarter" in description:
            return start + datetime.timedelta(hours=1)
        if "qtr" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=3)
    elif (sport == 'CBASE'):
        if "inning" in description:
            return start + datetime.timedelta(hours=1)
        if "atbat" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=3)
    elif (sport == 'MLB'):
        if "inning" in description:
            return start + datetime.timedelta(hours=1)
        if "atbat" in description:
            return start + datetime.timedelta(hours=1)
        if "plate appearance" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=3)
    elif (sport == 'NCB'):
        if "half" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=2)
    elif (sport == 'NCW'):
        if "half" in description:
            return start + datetime.timedelta(hours=1)
        if "quarter" in description:
            return start + datetime.timedelta(minutes=30)
        return start + datetime.timedelta(hours=2)
    elif (sport == 'NBA'):
        if "half" in description:
            return start + datetime.timedelta(hours=1)
        if "quarter" in description:
            return start + datetime.timedelta(minutes=30)
        if "qtr" in description:
            return start + datetime.timedelta(minutes=30)
        if "draft" in description:
            return start + datetime.timedelta(minutes=30)
        return start + datetime.timedelta(minutes=150)
    elif (sport == 'WNBA'):
        if "half" in description:
            return start + datetime.timedelta(hours=1)
        if "quarter" in description:
            return start + datetime.timedelta(minutes=30)
        return start + datetime.timedelta(hours=2)
    elif (sport == 'Hoops'):
        if "half" in description:
            return start + datetime.timedelta(hours=1)
        if "quarter" in description:
            return start + datetime.timedelta(minutes=30)
        if "qtr" in description:
            return start + datetime.timedelta(minutes=30)
        return start + datetime.timedelta(hours=2)
    elif (sport == 'Tennis'):
        if "set" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=2)
    elif (sport == 'NHL'):
        if "period" in description:
            return start + datetime.timedelta(hours=1)
        if "draft" in description:
            return start + datetime.timedelta(minutes=30)
        return start + datetime.timedelta(hours=3)
    elif (sport == 'Hockey'):
        if "period" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=3)
    elif (sport == 'Golf'):
        if "hole" in description:
            return start + datetime.timedelta(hours=1)
        if "par" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=4)
    elif (sport == 'Horse'):
        return start + datetime.timedelta(minutes=30)
    elif (sport == 'MMA'):
        return start + datetime.timedelta(hours=1)
    elif (sport == 'Boxing'):
        return start + datetime.timedelta(hours=1)
    elif (sport == 'Wrestling'):
        return start + datetime.timedelta(hours=1)
    elif (sport == 'NASCAR'):
        return start + datetime.timedelta(hours=4)
    elif (sport == 'EXPN'):
        return start + datetime.timedelta(hours=1)
    elif (sport == 'LAX'):
        return start + datetime.timedelta(hours=2)
    elif (sport == 'Rugby'):
        return start + datetime.timedelta(hours=2)
    elif (sport == 'ADHOC'):
        return start + datetime.timedelta(hours=2)
    elif (sport == 'AFL'):
        return start + datetime.timedelta(hours=2)
    elif (sport == 'Cycling'):
        return start + datetime.timedelta(hours=4)
    else:
        print('unknown sport ' + sport)
        return start + datetime.timedelta(hours=2)

def getMatchupByTime():
    endtime = datetime.datetime.max
    for matchup in root.iter("Matchup"):
        if (matchup.find('Locked').text == 'true'):
            continue
        matchuptime = endTime(matchup)
        if (matchuptime < endtime):
            endtime = matchuptime
            id = matchup.find('MatchupId').text
            percent = float(matchup.findall('Opponent')[0].find('PercentageUsersPicked').text)
            which = 0 if random.random() < percent else 1 # choose based on weighting of existing pickers
#                    which = random.randint(0, 1) # choose randomly
            oppId = matchup.findall('Opponent')[which].find('OpponentId').text
            makePick(id,oppId)
            print(matchup.find('Title').text)
            print(matchup.findall('Opponent')[which].find('Name').text)
            print(endtime)
	
def getMatchupByLeaderboard():
    try:
        tree = etree.parse("http://streak.espn.com/mobile/winLeaderboard")
        root = tree.getroot()
        for matchup in root.iter("LeaderBoardEntry"):
            if (not matchup.find('*//Locked') is None and matchup.find('*//Locked').text == 'false'):
                id = matchup.find('*//MatchupIdSelected').text
                oppId = matchup.find('*//OpponentIdSelected').text
                makePick(id,oppId)
                print(matchup.find('UserName').text)
                print(matchup.find('*//Title').text)
                break

    except Exception as ex:
        print(ex)

while(True):
    try:
        tree = etree.parse("http://streak.espn.com/mobile/viewMatchups?entryId=" + userInfo['entry'])
        root = tree.getroot()

        if (root.find('Entry').find('CurrentSelection') is None):
	        getMatchupByLeaderboard()
        	#getMatchupByTime()
    except ConnectionError: 
        print("connection error")
        pass
    except KeyError:
        print("key error")
        pass
    except OSError:
        print("OS error")
        pass
#    except XMLSyntaxError:
#        print("xml syntax error")
#        pass
    except Exception as ex:
        print("unknown error")
        print(ex)
        pass
    

    time.sleep(300)
