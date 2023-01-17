from urllib.request import Request, urlopen
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

# Links for football teams with exception of USA, Canada and Australia
exception_nation_links = {
    'Australia': "Australia_men%27s_national_soccer_team",
    'Canada': "Canada_men%27s_national_soccer_team",
    'United_States': "United_States_men%27s_national_soccer_team",
}

# Menu for a player's details
def playerSubMenu(playername, teamname):
    # replace space with underscore
    playername = playername.replace(' ', '_')
    # url for the player's wikipedia page
    link = 'https://en.wikipedia.org/wiki/{player}'.format(player=playername)
    # download the page
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = webpage.decode('utf-8')
    # save the page
    f = open('{player}.html'.format(player=playername), 'w',encoding='utf-8')
    f.write(data)
    f.close()
    # show the menu
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

# Menu to view details of a national team
def teamSubMenu(teamname):
    # replace space with underscore
    teamname = teamname.replace(' ', '_')
    # modifying url for the team's wikipedia page if it is USA, Canada or Australia
    if teamname in exception_nation_links:
        teamname = exception_nation_links[teamname]
    else:
        teamname += '_national_football_team'
    link = 'https://en.wikipedia.org/wiki/{nation}'.format(nation=teamname)
    print(link)
    # download the page
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = webpage.decode('utf-8')
    # save the page
    f = open('{nation}.html'.format(nation=teamname), 'w',encoding='utf-8')
    f.write(data)
    f.close()
    # show the menu
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
            # build lexer of the team's page and get the current squad
            squadlist = getCurrentSquad(teamname)
            print("************************************************************************")
            for i in range(0,len(squadlist)-1,2):
                print(str(i+1)+"."+squadlist[i] + "\t\t" + str(i+2) + "." + squadlist[i+1])
            print("************************************************************************")
            # logging the current squad
            with open('programlogs.txt', 'a') as programlogs:
                programlogs.write('Current Squad\t' + str(squadlist)+'\n')
        elif choice == 2:
            print('Last & upcoming five matches')
            # build lexer of the team's page and get the last & upcoming five matches
            getfivefixtures(teamname)
        elif choice == 3:
            squadlist = getCurrentSquad(teamname)
            print('Current Squad')
            squadlist = getCurrentSquad(teamname)
            print("************************************************************************")
            for i in range(0,len(squadlist)-1,2):
                print(str(i+1)+"."+squadlist[i] + "\t\t" + str(i+2) + "." + squadlist[i+1])
            print("************************************************************************")
            # playername = input('Enter the player name: ')
            # playerSubMenu(playername, teamname)
        elif choice == 4:
            # Exit
            mainmenu()
        else:
            print("Invalid choice!!")

# Menu to view details of knockout stages
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
        # build lexer of the knockout stage and get the fixtures and match details
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
        # show the menu for a particular knockout stage
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
                # print the fixtures
                print("*********************************************")
                for match in knockdata['matchlist']:
                    print(match)
                print("*********************************************")
                # logging the fixtures
                with open('programlogs.txt','a') as programlogs:
                    programlogs.write('Fixtures\t' + str(knockdata['matchlist'])+'\n')
            elif choice==2:
                # print the match details according to user's choice
                print("*********************************************")
                for match in knockdata['matchlist']:
                    print(match)
                print("*********************************************")
                matchchoice = int(input("Enter the match number: "))
                # check if the match number is valid
                if matchchoice > len(knockdata['matchlist']):
                    print("Enter a valid match number!")
                    continue
                # print the match details
                match = knockdata[str(matchchoice)]
                print("**************************************************************************************")
                print("Score: "+match['score'])
                print("Match details: "+match['details'])
                print("Scorers List: ",match['scorerlist'])
                print("Penalties: ",match['isPen'])
                print("Penalty takers: ",match['penscorers'])
                print("**************************************************************************************")
                # logging the match details
                with open('programlogs.txt','a') as programlogs:
                    programlogs.write('Match details\t' + str(match)+'\n')
            elif choice==3:
                break
            else:
                print("Invalid choice!!")

# Function to get a group's data
# this will build lexer of the group's page and get the fixtures and match details
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

# Menu to view details of group stages
def groupstageMenu():
    # get the group stage
    print('''
    Enter the stage you want to view (A/B/C/D/E/F/G/H):
    ''')
    stage = input()
    # check if the stage is valid
    if stage not in ['A','B','C','D','E','F','G','H']:
        print("Invalid stage")
        return
    # get the group data
    groupData = getGroupData(stage)
    # show the menu for a particular group stage
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
            # print the teams advanced for knockouts
            print("Teams advanced for knockouts")
            print("*****************************")
            print(groupData['pointtable'][0])
            print(groupData['pointtable'][1])
            print("*****************************")
            # logging the teams advanced for knockouts
            with open('programlogs.txt','a') as programlogs:
                programlogs.write('Teams advanced for knockouts\t' + str(groupData['pointtable'][0]) + '\t' + str(groupData['pointtable'][1])+'\n')
        elif choice == 2:
            # print the number of goals forwarded & conceded by teams
            print("Number of goals forwarded & conceded by teams")
            print("*********************************************")
            print("Team\tGF\tGC")
            for team in groupData['pointtable']:
                print(team)
            print("*********************************************")
            # logging the number of goals forwarded & conceded by teams
            with open('programlogs.txt','a') as programlogs:
                programlogs.write('Number of goals forwarded & conceded by teams\t' + str(groupData['pointtable'])+'\n')
        elif choice == 3:
            # print the match details according to user's choice
            print("*********************************************")
            for match in groupData['matchlist']:
                print(match)
            print("*********************************************")
            # get the match number
            matchchoice = int(input("Enter the match number: "))
            # check if the match number is valid
            if matchchoice > 8:
                print("Enter a valid match number")
                return
            # print the match details
            match = groupData['matches'][str(matchchoice)]
            print("**************************************************************************************")
            print("Score: "+match['score'])
            print("Match details: "+match['details'])
            print("Scorers List: ",match['scorers'])
            print("**************************************************************************************")
            # logging the match details
            with open('programlogs.txt','a') as programlogs:
                programlogs.write('Match details\t' + str(match)+'\n')
        elif choice==4:
            break
        else:
            print("Invalid choice!!")

# Menu to select which stage to view
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


# Main menu
def mainmenu():
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
        # build the lexer of the teams
        # print the teams participated in the tournament
        teamlist = getTeamList()
        print("*****************************************************************************************************************")
        for i in range(0,32,4):
            print(str(i+1)+"."+teamlist[i] + "\t\t" + str(i+2) + "." + teamlist[i+1] + "\t\t" + str(i+3) + "." + teamlist[i+2]+ "\t\t" + str(i+4) + "." + teamlist[i+3])
        print("*****************************************************************************************************************")
        # logging the teams participated in the tournament
        with open('programlogs.txt','a') as programlogs:
            programlogs.write('All the teams participated in the tournament are\t')
            programlogs.write(str(teamlist)+'\n')
    elif choice == 2:
        # build the lexer of the venues
        # print the venue details like name and capacity
        venueDict = getVenueList()
        print("****************************************************************************")
        for i in venueDict:
            print(i + " : " + venueDict[i])
        print("****************************************************************************")
        # logging the venue details like name and capacity
        with open('programlogs.txt','a') as programlogs:
            programlogs.write('Venue details like name and capacity\t')
            programlogs.write(str(venueDict)+'\n')
    elif choice == 3:
        # build the lexer of the matches of different stages
        print('Match details')
        stageMenu()
    elif choice == 4:
        # build the lexer of the awards
        winnerDict = getAwardsList()
        # print the awards
        print("****************************************************************************")
        for i in winnerDict:
            print(i + " \t\t\t: " + winnerDict[i])
        print("****************************************************************************")
        # logging the awards
        with open('programlogs.txt','a') as programlogs:
            programlogs.write('Awards List\t')
            programlogs.write(str(winnerDict)+'\n')
    elif choice == 5:
        # build the lexer of the teams
        teamlist = getTeamList()
        print("*****************************************************************************************************************")
        for i in range(0,32,4):
            print(str(i+1)+"."+teamlist[i] + "\t\t" + str(i+2) + "." + teamlist[i+1] + "\t\t" + str(i+3) + "." + teamlist[i+2]+ "\t\t" + str(i+4) + "." + teamlist[i+3])
        print("*****************************************************************************************************************")
        # get the team number
        teamnumber = int(input('Enter the team name (i.e. number): '))
        teamname = teamlist[teamnumber-1]
        with open('programlogs.txt','a') as teamlogs:
            teamlogs.write('Team name\t')
            teamlogs.write(teamname+'\n')
        # redirect to team sub menu for further choices
        teamSubMenu(teamname)
    elif choice == 6:
        exit()

if __name__ == '__main__':
    while True:
        mainmenu()