from flask import session
import json
from psycopg2 import pool
import requests
import math
SANhost = '192.168.2.94'
SANdb = 'sportsit_db'
DataCenterhost = '192.168.2.94'
DataCenterdb = 'datacenter'
dbuser = 'postgres'
dbpwd = 'root'
connection_pool_1 = pool.SimpleConnectionPool(1,10,host=SANhost, database=DataCenterdb, user=dbuser, password=dbpwd)
con_1=connection_pool_1.getconn()
cur_name1 = con_1.cursor()


def get_eachball_details(matchid,from_over,to_over):
    query = f"select * from cricket.eachball_data where matchid = '{matchid}' order by innings"
    cur_name1.execute(query)
    fetch_data = cur_name1.fetchall()
    if from_over<to_over:
        if len(fetch_data) >= from_over:
            if len(fetch_data) >= to_over:
                return fetch_data[from_over - 1:to_over]
            else:
                return fetch_data[from_over - 1:]
        else:
            return fetch_data
    else:
        return fetch_data

#print(get_eachball_details(1082591,5,40))


def get_batter_data(matchid):
    query1 = f"select * from cricket.batters_data where match_id = '{matchid}'"
    cur_name1.execute(query1)
    fetch_data = cur_name1.fetchall()
    print(fetch_data)
    return fetch_data


def get_bowler_data(matchid):
    query1 = f"select * from cricket.bolwers_data where match_id = '{matchid}'"
    cur_name1.execute(query1)
    fetch_data = cur_name1.fetchall()
    print(fetch_data)
    return fetch_data


#get_batter_data('1136612')


def eachover_count(matchid , from_over,to_over):
    eachball_details = get_eachball_details(matchid,from_over,to_over)
    l1 = []
    row_values = [x for x in range(6)]
    column_values = ['.',1,2,3,4,6,'other']
    for i in range(6):
        l2 = []
        for j in range(7):
            count = 0
            for ball_count in eachball_details:
                if ball_count[j+1]==i:
                    count+=1
            l2.append(count)
        l1.append(l2)
    percentage_values = []
    for i in l1:
        l2 = []
        for j in i:
            l2.append(float("{0:.1f}".format((j/len(eachball_details))*100)))
        percentage_values.append(l2)

    decimal_values = []
    for i in percentage_values:
        l2 = []
        for j in i:
            if int(j) == 0:
                l2.append(0)
            else:
                l2.append(float("{0:.1f}".format((1/j)*100)))
        decimal_values.append(l2)
    return [percentage_values , decimal_values,row_values,column_values]
#print(eachover_count(1082591,5,40))

def get_all_matches(season):
    query = f"select * from cricket.season_details where season_name='{season}'"
    cur_name1.execute(query)
    get_data = cur_name1.fetchall()
    all_data = []
    for i in range(0,len(get_data),2):
        matchid = get_data[i][-1]
        home_team_name = get_data[i][1]
        away_team_name = get_data[i][2]
        matchwinner = get_data[i][7]
        team_gender = get_data[i][5]
        kickoff = get_data[i][3]
        kickoff = kickoff.replace('[', '')
        kickoff = kickoff.replace(']', '')
        kickoff = kickoff.replace('"', '')
        matchtype = get_data[i][4]
        team_type = get_data[i][10]
        innings_data1 = json.loads(get_data[i][14])
        innings_data2 = json.loads(get_data[i+1][14])
        x= [matchwinner, team_gender, matchtype, team_type, innings_data1, innings_data2, home_team_name,
                away_team_name, kickoff, True]
        each_macth_data = get_eachball_details(matchid,0,0)

        all_data.append([x,[x[4],x[5]],matchid,each_macth_data])
    return all_data

def get_each_match(matchid):
    query = f"select * from cricket.season_details where matchid ='{matchid}'"
    cur_name1.execute(query)
    get_data = cur_name1.fetchall()
    print(get_data)
    if True:
        home_team_name =get_data[0][1]
        away_team_name = get_data[0][2]
        matchwinner = get_data[0][7]
        team_gender = get_data[0][5]
        kickoff = get_data[0][3]
        kickoff = kickoff.replace('[','')
        kickoff = kickoff.replace(']', '')
        kickoff = kickoff.replace('"','')
        matchtype = get_data[0][4]
        team_type = get_data[0][10]
        innings_data1 = json.loads(get_data[0][14])
        innings_data2 = json.loads(get_data[1][14])
        return [matchwinner,team_gender,matchtype,team_type,innings_data1, innings_data2, home_team_name,away_team_name,kickoff,True]
    # except Exception as error:
    #     print(error)
    #     return [False]
#print(get_each_match('1082591')[1])


def get_all_seasons():
    query = f"select season_name from cricket.season_details"
    cur_name1.execute(query)
    get_data = cur_name1.fetchall()
    all_seasons = []
    for season in get_data:
        all_seasons.append(season[0])
    return sorted(list(set(all_seasons)))


def all_home_teams(season_name):
    query = f"select home_team from cricket.season_details where season_name = '{season_name}'"
    cur_name1.execute(query)
    get_data = cur_name1.fetchall()
    all_teams = []
    for team in get_data:
        all_teams.append(team[0])
    return sorted(list(set(all_teams)))
def all_away_teams(season,home_team):
    query = f"select away_team from cricket.season_details where season_name = '{season}' and home_team='{home_team}'"
    cur_name1.execute(query)
    get_data = cur_name1.fetchall()
    all_teams = []
    for team in get_data:
        all_teams.append(team[0])
    return sorted(list(set(all_teams)))

def all_data(season_name,home_team,away_team):
    query = f"select * from cricket.season_details where" \
            f" season_name = '{season_name}'and home_team='{home_team}'and away_team = '{away_team}' order by matchid "
    cur_name1.execute(query)
    get_data = cur_name1.fetchall()
    get_matchid = get_data[0][16]
    try:
        innings_data1 = json.loads(get_data[0][14])
        innings_data2 = json.loads(get_data[1][14])
        return [get_data, innings_data1, innings_data2,get_matchid,True]
    except Exception as error:
        print(error)
        return [False]

def get_all_matchids(season):
    query = f"select matchid from cricket.season_details where season_name = '{season}'"
    cur_name1.execute(query)
    get_data = cur_name1.fetchall()
    all_matchids = []
    for matchid in get_data:
        all_matchids.append(matchid[0])
    return sorted(list(set(all_matchids)))

def cric_stats_center(home_team , away_team):
    query = f"select home_team, away_team, match_winner,stadium FROM cricket.season_details WHERE home_team ='{home_team}'and away_team = '{away_team}'"
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    home_team_win_count = 0
    away_team_win_count = 0
    new_match_data = []
    home_winning_count = 0
    away_winning_count = 0
    for match in fetc:
        each_match_data = []
        if match[2]==home_team:
            for i in match:
                each_match_data.append([i])
            home_team_win_count+=1
            each_match_data.append('W')
            each_match_data.append('L')
            new_match_data.append(each_match_data)
        else:
            each_match_data = []

            for i in match:
                each_match_data.append([i])
            each_match_data.append('L')
            each_match_data.append('W')
            new_match_data.append(each_match_data)
            away_team_win_count+=1
    return [new_match_data,home_team_win_count,away_team_win_count]


def get_all_teams():
    query = "select home_team,away_team from cricket.season_details"
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    all_teams_list = []
    for i in fetc:
        all_teams_list.append(i[0])
        all_teams_list.append(i[1])
    return list(set(all_teams_list))


def set_signin(request_form):
    userid = request_form.get('username')
    password = request_form.get('password')
    exist_user = is_exist_user(userid)
    if exist_user[0]:
        if password == exist_user[1]:

            # flash(f'Welcome {exist_user[2]}')
            return [True,exist_user[2]]
        else:
            # flash('Incorrect Password')
            return [False]
    else:
        # flash("UserId does' nt exists")
        return [False]


def is_exist_user(email):
    query1 = f"select * from master.signup where email = '{email}'"
    cur_name1.execute(query1)
    fetc = cur_name1.fetchall()
    print(fetc)
    password = ''
    user_name = ''
    try:
        if len(fetc)>0:
            exist_user = True
        else:
            exist_user =False
    except Exception as error:
        error=str(error)
        exist_user = False
    if exist_user:
        password = fetc[0][4]
        user_name = fetc[0][0]+' '+fetc[0][1]
    return [exist_user, password, user_name]




def get_each_batter_data(player_id):
    query = f"select * from cricket.batters_data where player_id ='{player_id}'"
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    data1 = []
    total_balls = 0
    total_runs = 0
    if len(fetc)>0:
        for i in fetc:
            total_balls+=i[3]
            total_runs+=i[2]
        strike_rate = "{:.2f}".format((total_runs /total_balls)*100)
        return [fetc[0][0], fetc[0][1], total_balls, total_runs, strike_rate]
    else:
        pass


def get_each_bolwer_data(player_id):
    query = f"select * from cricket.bolwers_data where player_id ='{player_id}'"
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    data1 = []
    total_overs = 0
    total_runs = 0
    wickets = 0
    if len(fetc)>0:
        for i in fetc:
            total_overs += round((i[2]/6))
            total_runs += i[4]
            wickets +=i[3]
        if total_runs==0 or total_overs==0:
            economy_rate = 0.00
        else:
            economy_rate = "{:.2f}".format(total_runs/total_overs)
        return [fetc[0][0],fetc[0][1],total_overs, total_runs,wickets, economy_rate]
    else:
        pass

def players_rating(players_list):
    batters_data = []
    for i in players_list:
        data1 = get_each_batter_data(i)
        if data1:
            batters_data.append(data1)
    bowlers_data = []
    for j in players_list:
        data2 = get_each_bolwer_data(j)
        if data2:
            bowlers_data.append(data2)
    return [batters_data,bowlers_data]

def players_list1():
    query = 'select * from cricket."Players_list" limit 11'
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    return fetc

def player_list2():
    query = 'select * from cricket."Players_list" limit 22'
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    return fetc[12:]


def top_batters():
    query = "select * from cricket.each_batters_total_data order by total_runs desc,total_balls limit 30"
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    return fetc

def top_bowlers():
    query = "SELECT *FROM cricket.each_bowler_data where  total_overs>100  order by economy_rate,avg_wicket_per_over limit 30;"
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    return fetc


def compare_batters_data(players_list1,player_list2):
    batters_data1 = players_rating(players_list1)[0]
    batters_data2 = players_rating(player_list2)[0]
    bowlers_data1=players_rating(players_list1)[1]
    bowlers_data2 = players_rating(player_list2)[1]
    top_batters_ids = list(map(lambda x: x[1],top_batters()))
    top_bowler_ids = list(map(lambda x:x[1],top_bowlers()))
    batters_data1 = []
    batters_data2 = []
    for id in players_list1:
        if id in top_batters_ids:
            batters_data1.append(id)
    for id in player_list2:
        if id in top_batters_ids:
            batters_data2.append(id)

    bolwers_data1_1 = []
    bolwers_data2_1 = []

    for id in players_list1:
        if id in top_bowler_ids:
            bolwers_data1_1.append(id)
    for id in player_list2:
        if id in top_bowler_ids:
            bolwers_data2_1.append(id)
    m1 = []
    if len(batters_data1)==len(batters_data2):
        indexes_count1 = 0
        indexes_count2 = 0
        for i in batters_data1:
            indexes_count1+=top_batters_ids.index(i)
        for i in batters_data2:
            indexes_count2+=top_batters_ids.index(i)
        if indexes_count1>indexes_count2:
            message1= f'Away Team have {len(batters_data2)} top battsmen'
        elif indexes_count1<indexes_count2:
            message1 = f'Home Team have {len(batters_data2)} top battsmen'
        else:
            message1 = f'Two teams Have top battesmen'

    else:
        if len(batters_data1)>len(batters_data2):
            message1= f'Home Team have More Batting lineup Then Away Team'
        else:
            message1 = f'Away Team have More Batting lineup Then Home Team'
    m1.append(message1)
    if len(bolwers_data1_1)==len(bolwers_data2_1):
        indexes_count1 = 0
        indexes_count2 = 0
        for i in bolwers_data1_1:
            indexes_count1+=top_bowler_ids.index(i)
        for i in bolwers_data2_1:
            indexes_count2+=top_bowler_ids.index(i)
        if indexes_count1>indexes_count2:
            message2= f'Away Team have {len(bolwers_data2_1)} top Bowlers'
        elif indexes_count1<indexes_count2:
            message2 = f'Home Team have {len(bolwers_data1_1)} top Bowlers'
        else:
            message2 = f'Two teams have top Bowlers'
    else:
        if len(bolwers_data1_1)>len(bolwers_data2_1):
            message2= f'Home Team have More Bowler lineup Then Away Team'
        else:
            message2 = f'Away Team have More Bolwer lineup Then Home Team'
    m2 = f'home team top batters:{len(batters_data1)}',f'away team top batters:{len(batters_data2)}'
    m3=f'home team top bowlers:{len(bolwers_data1_1)}',f'away team top bowlers:{len(bolwers_data2_1)}'
    m1.append(message2)
    m1.append(m2)
    m1.append(m3)
    return m1

def add_batters_data(player_id):
    query = f"select * from cricket.batters_data where player_id='{player_id}'"
    cur_name1.execute(query)
    fetc= cur_name1.fetchall()
    total_balls = 0
    total_runs=0
    total_matches=0
    if len(fetc)>0:
        for data in fetc:
            total_balls+=data[3]
            total_runs += data[2]
            total_matches+=1
        query1 = f"insert into cricket.each_batters_total_data values('{data[0]}','{data[1]}',{total_balls},{total_runs},{total_matches})"
        cur_name1.execute(query1)
        con_1.commit()

def players_list11():
    query = 'select * from cricket."Players_list"'
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    return fetc


def teams_players_list(team_name):
    query = f'select * from cricket."Players_list" '+f"where team_name = '{team_name}' and is_playing=1"
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    return fetc


def add_bowlers_data(player_id):
    query1 = f"select * from cricket.bolwers_data where player_id ='{player_id}'"
    total_overs=0
    total_runs=0
    total_wickets=0
    cur_name1.execute(query1)
    fetc = cur_name1.fetchall()
    if len(fetc)>0:
        for data in fetc:
            total_overs +=round(data[2]/6)
            total_runs+=data[4]
            total_wickets+=data[3]
        economy_rate = 0
        avg_wicket_per_over = 0
        if total_runs>0:
            if total_overs>0:
                economy_rate = total_runs/total_overs
                if total_wickets>0:
                    avg_wicket_per_over = total_overs/total_wickets
        query2 = f"insert into cricket.each_bowler_data values('{fetc[0][0]}','{fetc[0][1]}',{total_overs}," \
             f"{total_runs},{total_wickets},{economy_rate},{avg_wicket_per_over})"
        cur_name1.execute(query2)
        con_1.commit()

# for i in players_list11():
#     add_bowlers_data(i[1])

#print(teams_players_list('Chennai Super Kings'))

def add_player(player_id,team_id,team_name):
    query = f'update cricket."Players_list"'+f" set team_name='{team_name}',team_id = '{team_id}' where playerid ='{player_id}'"
    cur_name1.execute(query)
    con_1.commit()
#add_player('2efc430e',1)


#print(top_batters())
#print(compare_batters_data())
#print(players_rating(players_list()))
#print(players_list1())