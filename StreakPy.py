import requests
import json
from lxml import etree
import time
import datetime
import random

user = {
    'entry' : '547',
    'data' : '{"loginValue": "ggggooooggggoooo", "password": "ggooggoo"}'
    }
user = {
    'entry' : '9',
    'data' : '{"loginValue": "robbie_smith", "password": "kaurapo"}'
    }
def makePick(matchup, selection):
    try:
        s = requests.Session()
        r = s.post("https://registerdisney.go.com/jgc/v2/client/ESPN-ESPNCOM-PROD/guest/login", data = user['data'], headers = {'Content-Type': 'application/json' })

        accountInfo = json.loads(r.text)

        s.cookies.update({'swid': accountInfo['data']['profile']['swid']})
        s.cookies.update({'espn_s2': accountInfo['data']['s2']})

        page = s.get('http://streak.espn.go.com/en/createOrUpdateEntry?matchup=m' + matchup + 'o' + selection)

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
        return start + datetime.timedelta(hours=2)
    elif (sport == 'NFL'):
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
        return start + datetime.timedelta(hours=3)
    elif (sport == 'NCB'):
        if "half" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=2)
    elif (sport == 'NCW'):
        if "half" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=2)
    elif (sport == 'NBA'):
        if "half" in description:
            return start + datetime.timedelta(hours=1)
        if "quarter" in description:
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
        return start + datetime.timedelta(hours=2)
    elif (sport == 'Tennis'):
        if "set" in description:
            return start + datetime.timedelta(hours=1)
        return start + datetime.timedelta(hours=2)
    elif (sport == 'NHL'):
        if "period" in description:
            return start + datetime.timedelta(hours=1)
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
    elif (sport == 'NASCAR'):
        return start + datetime.timedelta(hours=4)
    elif (sport == 'EXPN'):
        return start + datetime.timedelta(hours=1)
    elif (sport == 'Rugby'):
        return start + datetime.timedelta(hours=2)
    elif (sport == 'ADHOC'):
        return start + datetime.timedelta(hours=2)
    else:
        print('unknown sport ' + sport)
        return start + datetime.timedelta(hours=3)

while(True):
    try:
        tree = etree.parse("http://streak.espn.go.com/mobile/viewMatchups?entryId=" + user['entry'])

        root = tree.getroot()

        if (root.find('Entry').find('CurrentSelection') is None):
            endtime = datetime.datetime.max
            for matchup in root.iter("Matchup"):
                if (matchup.find('Locked').text == 'true'):
                    continue
                matchuptime = endTime(matchup)
                if (matchuptime < endtime):
                    endtime = matchuptime
                    id = matchup.find('MatchupId').text
                    percent = float(matchup.findall('Opponent')[0].find('PercentageUsersPicked').text)
                    which = 0 if random.random() < percent else 1
#                    which = random.randint(0, 1)
                    oppId = matchup.findall('Opponent')[which].find('OpponentId').text
                    makePick(id,oppId)
                    print(matchup.find('Title').text)
                    print(matchup.findall('Opponent')[which].find('Name').text)
                    print(endtime)
    except ConnectionError: 
        print("connection error")
        pass
    except KeyError:
        print("key error")
        pass
    except OSError:
        print("OS error")
        pass

    time.sleep(300)
