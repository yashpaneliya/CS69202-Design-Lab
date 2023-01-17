from urllib.request import Request, urlopen
import logging
from teamyacc2 import getTeamList
from venueyacc import getVenueList
from awardsyacc import getAwardsList
from nationyacc import getCurrentSquad
from fivefict import getfivefixtures

from groupA import groupA
from groupB import groupB
from groupC import groupC
from groupD import groupD
from groupE import groupE
from groupF import groupF
from groupG import groupG
from groupH import groupH

from round16 import round16
from semifinals import semiFinals
from quarterfinals import quarterfinals
from thirdplace import thirdPlace
from finals import final

from ply.lex import lex
from ply.yacc import yacc

exception_nation_links = {
    'Australia': "Australia_men%27s_national_soccer_team",
    'Canada': "Canada_men%27s_national_soccer_team",
    'United_States': "United_States_men%27s_national_soccer_team",
}

# Write a menu-driven program to resolve user queries in simple python
# Queries can be from below list:
# a. All the teams participated in the tournament.
# b. Venue details like name and capacity.
# c. Match details
    # i. Group stage
    # ii. Knockout stage
    # Here for a given group and a specific match below details:
    # 1. Stadium detail
    # 2. Attendance
    # 3. Goal scorer(if any)
    # 4. Referee
    # Also given a group name:
    # 1. Teams advanced for knockouts.
    # 2. Given a team name, the number of goals forwarded & conceded.
    # For knockout stages:
    # 1. Show the fixtures
    # 2. Given two countries:
        # a. Results
        # b. Scorer
        # c. Stadium
        # d. Attendance
        # e. Referee
# d.    Show all the awards
# e.    Given a team name:
        # 1. Show its current squad.
        # 2. Show its last & upcoming five matches.
        # 3. Given a player name from the current squad.
            # a. Show his DoB
            # b. Playing position
            # c. Current club
            # d. Past clubs
            # e. International appearance
            # f. Goal count

# user will enter the query number and according to that the subquery list will prompt (if any) and then user will provide input (if required) and result will be displayed
log = open('log.txt', 'w', encoding='utf-8')

def playerSubMenu(playername, teamname):
    # replace space with underscore
    playername = playername.replace(' ', '_')
    link = 'https://en.wikipedia.org/wiki/{player}'.format(player=playername)
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = webpage.decode('utf-8')
    f = open('{player}.html'.format(player=playername), 'w',encoding='utf-8')
    f.write(data)
    f.close()

    print('''
    ******************************************
    1. Show DoB
    2. Playing position
    3. Current club
    4. Past clubs
    5. International appearance
    6. Goal count
    7. Exit
    ******************************************
    ''')
    choice = int(input('Enter your choice: '))
    if choice == 1:
        print('DoB')
    elif choice == 2:
        print('Playing position')
    elif choice == 3:
        print('Current club')
    elif choice == 4:
        print('Past clubs')
    elif choice == 5:
        print('International appearance')
    elif choice == 6:
        print('Goal count')
    elif choice == 7:
        teamSubMenu(teamname)


def teamSubMenu(teamname):
    # replace space with underscore
    teamname = teamname.replace(' ', '_')
    if teamname in exception_nation_links:
        teamname = exception_nation_links[teamname]
    else:
        teamname += '_national_football_team'
    link = 'https://en.wikipedia.org/wiki/{nation}'.format(nation=teamname)
    print(link)
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = webpage.decode('utf-8')
    f = open('{nation}.html'.format(nation=teamname), 'w',encoding='utf-8')
    f.write(data)
    f.close()
    while True:
        print('''
        *******************************************************
        1. Show its current squad.
        2. Show its last & upcoming five matches.
        3. View player details
        4. Exit
        *******************************************************
        ''')
        choice = int(input('Enter your choice: '))
        if choice == 1:
            print('Current Squad')
            squadlist = getCurrentSquad(teamname)
            print("************************************************************************")
            for i in range(0,len(squadlist)-1,2):
                print(str(i+1)+"."+squadlist[i] + "\t\t" + str(i+2) + "." + squadlist[i+1])
            print("************************************************************************")
        elif choice == 2:
            print('Last & upcoming five matches')
            getfivefixtures(teamname)
        elif choice == 3:
            squadlist = getCurrentSquad(teamname)
            print('Current Squad')
            squadlist = getCurrentSquad(teamname)
            print("************************************************************************")
            for i in range(0,len(squadlist)-1,2):
                print(str(i+1)+"."+squadlist[i] + "\t\t" + str(i+2) + "." + squadlist[i+1])
            print("************************************************************************")
            playername = input('Enter the player name: ')
            playerSubMenu(playername, teamname)
        elif choice == 4:
            mainmenu()
        else:
            print("Invalid choice!!")

def knockstageMenu():
    while True:
        print('''
        ************************************************
        * 1. Round of 16                               *
        * 2. Quarter finals                            *
        * 3. Semi finals                               *
        * 4. Third place                               *
        * 5. Final                                     *
        * 6. Exit                                      *
        ************************************************
        ''')
        ks = int(input("Select the knockout stage:"))
        if ks == 1:
            knockdata = round16()
        elif ks ==2:
            knockdata = quarterfinals()
        elif ks==3:
            knockdata = semiFinals()
        elif ks==4:
            knockdata = thirdPlace()
        elif ks==5:
            knockdata = final()
        elif ks==6:
            break
        else:
            print("Invalid choice!!")
            continue
        while True:
            print('''
            *****************************************************************
            * 1. Fixtures                                                   *
            * 2. Match details                                              *
            * 3. Exit                                                       *
            *****************************************************************
            ''')
            choice = int(input("Enter the choice: "))
            if choice==1:
                print("*********************************************")
                for match in knockdata['matchlist']:
                    print(match)
                print("*********************************************")
            elif choice==2:
                print("*********************************************")
                for match in knockdata['matchlist']:
                    print(match)
                print("*********************************************")
                matchchoice = int(input("Enter the match number: "))
                if matchchoice > len(knockdata['matchlist']):
                    print("Enter a valid match number!")
                    continue
                match = knockdata[str(matchchoice)]
                print("**************************************************************************************")
                print("Score: "+match['score'])
                print("Match details: "+match['details'])
                print("Scorers List: ",match['scorerlist'])
                print("Penalties: ",match['isPen'])
                print("Penalty takers: ",match['penscorers'])
                print("**************************************************************************************")
            elif choice==3:
                break
            else:
                print("Invalid choice!!")

def getGroupData(stage):
    if stage == 'A':
        return groupA()
    elif stage == 'B':
        return groupB()
    elif stage == 'C':
        return groupC()
    elif stage == 'D':
        return groupD()
    elif stage == 'E':
        return groupE()
    elif stage == 'F':
        return groupF()
    elif stage == 'G':
        return groupG()
    elif stage == 'H':
        return groupH()

def groupstageMenu():
    print('''
    Enter the stage you want to view (A/B/C/D/E/F/G/H):
    ''')
    stage = input()
    if stage not in ['A','B','C','D','E','F','G','H']:
        print("Invalid stage")
        return
    groupData = getGroupData(stage)
    while True:
        print('''
        *****************************************************************
        * 1. Teams advanced for knockouts.                              *
        * 2. Number of goals forwarded & conceded by teams              *
        * 3. Match details                                              *
        * 4. Exit                                                       *
        *****************************************************************
        ''')
        choice = int(input("Enter choice: "))
        if choice == 1:
            print("Teams advanced for knockouts")
            print("*****************************")
            print(groupData['pointtable'][0])
            print(groupData['pointtable'][1])
            print("*****************************")
        elif choice == 2:
            print("Number of goals forwarded & conceded by teams")
            print("*********************************************")
            print("Team\tGF\tGC")
            for team in groupData['pointtable']:
                print(team)
            print("*********************************************")
        elif choice == 3:
            print("*********************************************")
            for match in groupData['matchlist']:
                print(match)
            print("*********************************************")
            matchchoice = int(input("Enter the match number: "))
            if matchchoice > 8:
                print("Enter a valid match number")
                return
            match = groupData['matches'][str(matchchoice)]
            print("**************************************************************************************")
            print("Score: "+match['score'])
            print("Match details: "+match['details'])
            print("Scorers List: ",match['scorers'])
            print("**************************************************************************************")
        elif choice==4:
            break
        else:
            print("Invalid choice!!")

def stageMenu():
    while True:
        print('''
        *********************************
        * 1. Group Stage                *
        * 2. Knockout Stage             *
        * 3. Exit                       *
        *********************************
        ''')
        stage = int(input("Select the stage:"))
        if stage==1:
            groupstageMenu()
        elif stage==2:
            knockstageMenu()
        elif stage==3:
            break
        else:
            print("Invalid choice!!")

def mainmenu():
    global log
    print('''
    *****************************************************************
    * 1. All the teams participated in the tournament.              *
    * 2. Venue details like name and capacity.                      *
    * 3. Match details                                              *
    * 4. Show all the awards                                        *
    * 5. View team details                                          *
    * 6. Exit                                                       *
    *****************************************************************
    ''')
    choice = int(input('Enter your choice: '))
    if choice == 1:
        teamlist = getTeamList()
        print("*****************************************************************************************************************")
        for i in range(0,32,4):
            print(str(i+1)+"."+teamlist[i] + "\t\t" + str(i+2) + "." + teamlist[i+1] + "\t\t" + str(i+3) + "." + teamlist[i+2]+ "\t\t" + str(i+4) + "." + teamlist[i+3])
        print("*****************************************************************************************************************")
        log.write('All the teams participated in the tournament are: ')
        log.write(str(teamlist))
    elif choice == 2:
        venueDict = getVenueList()
        print("****************************************************************************")
        for i in venueDict:
            print(i + " : " + venueDict[i])
        print("****************************************************************************")
        log.write('Venue details like name and capacity are: ')
        log.write(str(venueDict))
    elif choice == 3:
        print('Match details')
        stageMenu()
    elif choice == 4:
        winnerDict = getAwardsList()
        print("****************************************************************************")
        for i in winnerDict:
            print(i + " \t\t\t: " + winnerDict[i])
        print("****************************************************************************")
        log.write('Awards List')
        log.write(str(winnerDict))
    elif choice == 5:
        teamlist = getTeamList()
        print("*****************************************************************************************************************")
        for i in range(0,32,4):
            print(str(i+1)+"."+teamlist[i] + "\t\t" + str(i+2) + "." + teamlist[i+1] + "\t\t" + str(i+3) + "." + teamlist[i+2]+ "\t\t" + str(i+4) + "." + teamlist[i+3])
        print("*****************************************************************************************************************")
        teamnumber = int(input('Enter the team name (i.e. number): '))
        teamname = teamlist[teamnumber-1]
        log.write('Team name: ')
        log.write(teamname)
        teamSubMenu(teamname)
    elif choice == 6:
        exit()

if __name__ == '__main__':
    while True:
        mainmenu()