import os
import threading,concurrent.futures
import json
import time,datetime
from psycopg2 import pool
SANhost = '192.168.2.94'
SANdb = 'sportsit_db'
DataCenterhost = '192.168.2.94'
DataCenterdb = 'datacenter'
dbuser = 'mohan'
dbpwd = 'Nmohan_1'
connection_pool_1 = pool.SimpleConnectionPool(1,10,host=SANhost, database=DataCenterdb, user=dbuser, password=dbpwd)
con_1=connection_pool_1.getconn()
cur_name1 = con_1.cursor()

def get_file_data(file_id):
    if True:
        file_name = file_id+'.json'
        if True:
            open_file = open('ipl_json/'+str(file_name),'r')
            read_file = json.load(open_file)
            open_file.close()
            player_names = []
            home_team_palyer_names = []
            away_team_palayer_name = []
            season = str(read_file['info']['season'])
            team_names = list(read_file['info']['players'].keys())
            home_team_name = team_names[0].replace("'",'"')
            away_team_name = team_names[1].replace("'",'"')
            print(home_team_name,away_team_name)
            # if search_home_team_name.lower() in home_team_name.lower() or search_home_team_name.lower() in away_team_name :
            #     if search_away_team_name.lower() in home_team_name.lower() or search_away_team_name.lower() in away_team_name.lower():
            home_team_playes = read_file['info']['players'][home_team_name]
            away_team_players = read_file['info']['players'][away_team_name]
            stadium_name = read_file['info']['venue'].replace("'",'')
            palyers_ids = read_file['info']['registry']['people']
            # stadium_city_name = read_file['info']['city']
            match_start_date = read_file['info']['dates']
            players_gender = read_file['info']['gender']
            if 'event' in list(read_file['info'].keys()):
                match_type = read_file['info']['event']['name']
            else:
                match_type = read_file['info']['match_type']
            team_type = read_file['info']['team_type']
            # tournaments insert
            cur_name1.execute('select tournament_id from cricket.tournaments')
            fetc = cur_name1.fetchall()
            length_of_ids = len(fetc)
            tournament_ids = []
            for x in fetc:
                tournament_ids.append(x[0])
            increment_id = 0
            while True:
                increment_id+=1
                if length_of_ids+increment_id in tournament_ids:
                    pass
                else:
                    tournament_id = length_of_ids+increment_id
                    break
            query1 = f"insert into cricket.tournaments values ('{match_type}',{tournament_id},'{season}','{team_type}')"
            cur_name1.execute(query1)
            con_1.commit()
            # =====================
            # enter players list
            enter_player_list(file_name,tournament_id)
            # ===========================
            # match_type_number = read_file['info']['match_type_number']
            # winning_team_runs_lead = read_file['info']['outcome']['by']['runs']
            try:
                winning_team = read_file['info']['outcome']['winner']
            except:
                winning_team = read_file['info']['outcome']['result']

            if 'Test'.lower() in match_type.lower():
                number_of_overs=None
            else:
                number_of_overs = read_file['info']['overs']
            try:
                player_of_match = read_file['info']['player_of_match'][0].replace("'",'"')
            except:
                player_of_match ="missing"
            toss_won_team = read_file['info']['toss']['winner']
            toss_dession = read_file['info']['toss']['decision']
            innings_details = read_file['innings']
            all_overs = []
            overs_count = 0
            innings_count = 1
            # ======
            people_list_json = read_file['info']['registry']['people']
            players_list = list(people_list_json.keys())
            players_ids = list(people_list_json.values())
            batters_score = {}
            batters_play_balls ={}
            bowler_overs ={}
            bowlers_score = {}
            bowler_taken_number_of_wickets = {}
            bowler_taken_wicket_at_over_number ={}
            for player_name in players_list:
                batters_score[player_name] = 0
                batters_play_balls[player_name]=0
                bowlers_score[player_name]=0
                bowler_overs[player_name]=0
                bowler_taken_number_of_wickets[player_name] = 0
                bowler_taken_wicket_at_over_number[player_name] = []

            # ====
            for innings in innings_details:
                total_score = 0
                innings_all_over = []
                overs = innings['overs']
                for over in overs:
                    each_over_score =0
                    overnumber = over['over']
                    over_number = over['over']
                    deliveries = over['deliveries']
                    over_details =[]
                    over_details.append(over_number)
                    ball_count = 0
                    dot_ball = 0
                    ones = 0
                    twos = 0
                    threes = 0
                    fours = 0
                    sixes = 0
                    extras = 0
                    wickets = 0
                    count = 0
                    correct_deliveries = 0
                    for delivery in deliveries:
                        batters_score[delivery['batter']] +=delivery['runs']['batter']
                        count +=1
                        runs_data = delivery['runs']
                        if int(runs_data['extras']) > 0:
                            extras+=int(runs_data['extras'])
                            if 'legbyes' in list(delivery['extras'].keys()):
                                batters_play_balls[delivery['batter']] += 1
                                correct_deliveries+=1
                        else:
                            batters_play_balls[delivery['batter']] += 1
                            correct_deliveries += 1
                        if int(runs_data['total']) ==0:
                            dot_ball+=1
                        if int(runs_data['batter'])==0:
                            pass
                        elif int(runs_data['batter']) ==1:
                            ones +=1
                        elif int(runs_data['batter']) ==2:
                            twos +=1
                        elif int(runs_data['batter']) == 3:
                            threes +=1
                        elif int(runs_data['batter']) == 4:
                            fours +=1
                        elif int(runs_data['batter']) >= 6:
                            sixes += 1
                        each_over_score += int(runs_data['total'])
                        if 'wickets' in list(delivery.keys()):
                            wickets += 1
                            bowler_taken_number_of_wickets[delivery['bowler']] += 1
                            bowler_taken_wicket_at_over_number[delivery['bowler']].\
                                append(bowler_overs[deliveries[0]['bowler']]+(correct_deliveries/10))
                        bowlers_score[deliveries[0]['bowler']] += int(runs_data['total'])
                    bowler_overs[deliveries[0]['bowler']] += correct_deliveries
                    query = f"insert into cricket.eachball_data values({overnumber},{dot_ball},{ones},{twos},{threes},{fours},{sixes},{extras},{wickets},{each_over_score},{innings_count},'{file_id}')"
                    cur_name1.execute(query)
                    each_over_score += int(delivery['runs']['total'])
                    total_score+= each_over_score
                    #over_details.append(delivery_details)
                    over['over_score']= each_over_score
                # print(bowler_overs)
                # print(bowler_taken_wicket_at_over_number)
                # print(bowlers_score)
                # print(bowler_taken_number_of_wickets)
                innings['innings_total_run'] = total_score
                innings_all_over= str(innings)
                players_list = list(read_file['info']['registry']['people'].keys())
                seperrate_list = []
                for player in players_list:
                    if "'" in player:
                        a1 = player.replace("'",'')
                        innings_all_over = innings_all_over.replace(player,a1)
                    elif '"' in player:
                        a1 = player.replace('"','')
                        innings_all_over = innings_all_over.replace(player, a1)
                innings_all_over = innings_all_over.replace("'", '"')
                innings_all_over = innings_all_over.replace('True','"True"')
                date_details = str(match_start_date)
                #print(innings_all_over)
                date_details = date_details.replace("'",'"')
                a = open('1.json','w')
                a.write(json.dumps(innings_all_over))
                a.close()
                c_1 = open('1.json','r')
                c_2 = json.loads(c_1.read())
                query = f"insert into cricket.season_details values('{season}','{home_team_name}','{away_team_name}','{date_details}','{match_type}','{players_gender}','{player_of_match}','{winning_team}','{toss_won_team}','{toss_dession}','{number_of_overs}'," \
                        f"'{team_type}','{stadium_name}','{innings_count}','{innings_all_over}',{total_score},'{file_id}');"
                cur_name1.execute(query)
                con_1.commit()
                innings_count += 1
        for i in range(len(players_list)):
            player_name = players_list[i]
            strike_rate = 0
            economic_rate = 0
            if bowler_overs[player_name]>0:
                economic_rate = "{:.2f}".format(bowlers_score[player_name]/(bowler_overs[player_name]/6))
                query1 = f"insert into cricket.bolwers_data values('{player_name}','{players_ids[i]}',{bowler_overs[player_name]},{bowler_taken_number_of_wickets[player_name]},{bowlers_score[player_name]},'{season}',{file_id},{economic_rate})"
                cur_name1.execute(query1)
                con_1.commit()
            if batters_play_balls[player_name] > 0:

                # add data to each batter data table
                # add_batters_data(batters_play_balls[player_name],players_ids[i],batters_play_balls[player_name],batters_score[player_name])
                # ===========


                strike_rate = "{:.2f}".format((batters_score[player_name] /batters_play_balls[player_name])*100)

                query = f"insert into cricket.batters_data values ('{player_name}','{players_ids[i]}'," \
                        f"{batters_score[player_name]},{batters_play_balls[player_name]},'{season}','{file_id}',{strike_rate})"
                cur_name1.execute(query)
                con_1.commit()
    return 'Completed'


def enter_player_list(file_name,tournament_id):
    query = 'select playerid from cricket."Players_list"'
    cur_name1.execute(query)
    fetch_data = cur_name1.fetchall()
    existed_players_list = []
    for list1 in fetch_data:
        existed_players_list.append(list1[0])
    open_file = open('ipl_json/' + str(file_name), 'r')
    read_file = json.load(open_file)
    open_file.close()
    list_json = read_file['info']['registry']['people']
    players_list = list(list_json.keys())
    players_ids = list(list_json.values())
    batters_score = {}
    for player_name in players_list:
        batters_score[player_name] = 0
    for i in range(len(players_ids)):
        if players_ids[i] in  existed_players_list:
            pass
        else:
            insert_query = f'insert into cricket."Players_list" values'+f"('{players_list[i]}','{players_ids[i]}',{tournament_id})"
            cur_name1.execute(insert_query)
            con_1.commit()


def dump_data_into_db():
    dir_lists = sorted(os.listdir(r'C:\Users\User 101\Desktop\automation projects\cricket_scrape\ipl_json'))
    count = 0
    query = "select matchid from cricket.eachball_data"
    cur_name1.execute(query)
    a = cur_name1.fetchall()
    b = []
    c = []
    for i in a:
        b.append(i[0])
    count = 0
    for file_name in dir_lists:
        if '.json' in file_name:
            file_id = file_name.replace('.json', '')
            if file_id in b:
                pass
            else:
                print(file_id)
                get_file_data(file_id)
                count+=1
                if count ==100:
                    break


def add_batters_data(player_name,player_id,total_balls,total_runs):
    query1 = f"select * from cricket.each_batters_total_data where player_id='{player_id}'"
    cur_name1.execute(query1)
    fetc1 = cur_name1.fetchall()
    if len(fetc1)>0:
        total_matches = 0
        for data in fetc1:
            total_balls += data[2]
            total_runs += data[3]
            total_matches = data[4]+1
        query2 = f"update cricket.each_batters_total_data set total_balls={total_balls} , total_runs={total_runs} , number_of_matches={total_matches+1}"
        cur_name1.execute(query2)
        con_1.commit()
    else:
        query1 = f"insert into cricket.each_batters_total_data values('{player_name}','{player_id}',{total_balls},{total_runs},1)"
        cur_name1.execute(query1)
        con_1.commit()


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
        query2 = f"insert into cricket.each_bowler_data values('{fetc[0][0]}','{fetc[0][1]}',{total_overs}," \
             f"{total_runs},{total_wickets})"
        cur_name1.execute(query2)
        con_1.commit()



#add_bowlers_data('1abb78f8')
# con_1.close()
# dump_data_into_db()
# get_data_from_db()

