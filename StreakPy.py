import requests
import json
from lxml import etree
import time
import datetime
import random
import user
from selenium import webdriver


userInfo = user.getUser()

def makePick(matchup, selection):
    try:
        driver = webdriver.Chrome()
        driver.get('http://espn.com/login')
        time.sleep(2)
        # C:\Users\robsmith\AppData\Local\Microsoft\WindowsApps
        driver.switch_to.frame(driver.find_element_by_id("disneyid-iframe"))
#        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
#        driver.switch_to.frame(driver.find_element_by_name("disneyid-iframe"))
        driver.find_element_by_xpath("//input[@type='email']").send_keys(userInfo['data']['loginValue']);
        driver.find_element_by_xpath("//input[@type='password']").send_keys(userInfo['data']['password']);
        driver.find_element_by_xpath("//button[@type='submit']").click();
        time.sleep(2)
        driver.get('http://fantasy.espn.com/streak/en/createOrUpdateEntry?matchup=m' + matchup + 'o' + selection)
        time.sleep(2)
        driver.close()
        
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
#                    which = random.randint(0, 1) # choose randomly with equal probability
            oppId = matchup.findall('Opponent')[which].find('OpponentId').text
            makePick(id,oppId)
            print(matchup.find('Title').text)
            print(matchup.findall('Opponent')[which].find('Name').text)
            print(endtime)
	
def getMatchupByLeaderboard():
    parser = etree.XMLParser(recover=True)
    tree = etree.parse("http://fantasy.espn.com/streak/en/mobile/winLeaderboard", parser)
    root = tree.getroot()
    for matchup in root.iter("LeaderBoardEntry"):
        if (not matchup.find('*//Locked') is None and matchup.find('*//Locked').text == 'false'):
            id = matchup.find('*//MatchupIdSelected').text
            oppId = matchup.find('*//OpponentIdSelected').text
            makePick(id,oppId)
            print(matchup.find('UserName').text)
            print(matchup.find('*//Title').text)
            break

while(True):
    try:
        tree = etree.parse("http://fantasy.espn.com/streak/en/mobile/viewMatchups?entryId=" + userInfo['entry'])
        root = tree.getroot()

        if (root.find('Entry').find('CurrentSelection') is None):
            if datetime.datetime.today().day == 1:
                getMatchupByTime()
            else:
                getMatchupByLeaderboard()

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
