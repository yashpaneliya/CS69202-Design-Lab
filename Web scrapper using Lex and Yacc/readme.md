# Web scrapper using Lex and Yacc

## Problem Statement

Develop a web crawler and extract the required information by creating suitable grammar rules. The crawler is built to extract all the details related FIFA World Cup 2022 from its wikipedia [page](https://en.wikipedia.org/wiki/2022_FIFA_World_Cup).

This is a menu driven program which has the following functionalities:
1. Display the list of all the teams participating in the FIFA World Cup 2022
2. Display the list of all the stadiums (with capacity) where the matches were played
3. Match details
    - Group stage
    - Knockout stage

    For a given group:
    - Team advanced to knockouts
    - Given a team name, the number of goals forwarded & conceded

    For given a match in group:
    - Stadium detail
    - Attendance
    - Goal scorer(if any)
    - Referee

    For knockout stage:
    - Show fixtures
    - Given two countries:
        - Results
        - Scorer
        - Stadium
        - Attendance
        - Referee
4. Awards
5. Given a team name:
    - Squad
    - Last and upcoming 5 matches in any league or tournament
    - Given a player name:
        - DoB
        - Position
        - Club
        - Past clubs
        - International appearances
        - Goal counts

## Code walk-through

- The code is divided into several parts according to each functionality mentioned above.

- Each file contains lex and yacc code for the corresponding functionality.

- `menu.py` contains the driver code.

- All the lowercase are variables and uppercase are terminals in the grammar rules.

- Lex section contains the regular expressions for the tokens
  ```python
  # regex to find h3 tag of stadiums in web page
  def t_BEGINVENUE(t):
    '''<h3><span\sclass="mw-headline"\sid="Stadiums">Stadiums</span></h3>'''
    return t
  ```

- Yacc section contains the grammar rules and the actions to be performed when a rule is matched
  ```python
    # grammar to extract stadium details and store it
    def p_columns(p):
        '''columns : OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT skip CLOSEDATA'''
        if len(p)==10:
            venue[p[3]] = p[7]
  ```

## How to run

- Install ply using `pip install ply`
- Run `python menu.py` to start the program
- Enter the choice of functionality to be performed
- Enter the required input

## Output

```bash
PS D:\MTech\Sem_2\Design Lab\A2\Scrapper> py menu.py

    *****************************************************************
    * 1. All the teams participated in the tournament.              *
    * 2. Venue details like name and capacity.                      *
    * 3. Match details                                              *
    * 4. Show all the awards                                        *
    * 5. View team details                                          *
    * 6. Exit                                                       *
    *****************************************************************
    
Enter your choice: 1

*****************************************************************************************************************
1.Argentina             2.Australia             3.Belgium               4.Brazil
5.Cameroon              6.Canada                7.Costa Rica            8.Croatia
9.Denmark               10.Ecuador              11.England              12.France
13.Germany              14.Ghana                15.Iran                 16.Japan
17.Mexico               18.Morocco              19.Netherlands          20.Poland
21.Portugal             22.Qatar                23.Saudi Arabia         24.Senegal
25.Serbia               26.South Korea          27.Spain                28.Switzerland
29.Tunisia              30.United States        31.Uruguay              32.Wales
*****************************************************************************************************************

Enter your choice: 4

****************************************************************************
Golden Ball                     : Lionel Messi
Silver Ball                     : Kylian Mbappé
Bronze Ball                     : Luka Modrić
Golden Boot                     : Kylian Mbappé
Silver Boot                     : Lionel Messi
Bronze Boot                     : Olivier Giroud
Golden Glove                    : Emiliano Martínez
FIFA Young Player Award         : Enzo Fernández
FIFA Fair Play Trophy           : England
****************************************************************************

Enter your choice: 3
Match details

        *********************************
        * 1. Group Stage                *
        * 2. Knockout Stage             *
        * 3. Exit                       *
        *********************************

Select the stage:1

    Enter the stage you want to view (A/B/C/D/E/F/G/H): A


        *****************************************************************
        * 1. Teams advanced for knockouts.                              *
        * 2. Number of goals forwarded & conceded by teams              *
        * 3. Match details                                              *
        * 4. Exit                                                       *
        *****************************************************************

Enter choice: 3
*********************************************
Qatar 0-2 Equador
Senegal 0–2 Netherlands
Qatar 1–3 Senegal
Netherlands 1–1 Ecuador
Ecuador 1–2 Senegal
Netherlands 2–0 Qatar
*********************************************
Enter the match number: 1
**************************************************************************************
Score: Qatar 0-2 Equador
Match details: Al Bayt Stadium ,  Al Khor Attendance: 67,372 Referee:  Daniele Orsato
Scorers List:  ['Valencia']
**************************************************************************************

Select the stage:2

        ************************************************
        * 1. Round of 16                               *
        * 2. Quarter finals                            *
        * 3. Semi finals                               *
        * 4. Third place                               *
        * 5. Final                                     *
        * 6. Exit                                      *
        ************************************************

Select the knockout stage:5
```
*P.S. Everyone knows the results of the final match 😉😉*
