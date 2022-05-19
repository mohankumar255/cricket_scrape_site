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

query = "select matchid from cricket.eachball_data"
cur_name1.execute(query)
a = cur_name1.fetchall()
b = []
c=[]
for i in a:
    b.append(i[0]+'.json')
def get_file_data(file_name):
    if '.json' in file_name:
        is_file = False
        file_id = file_name.replace('.json','')
        if file_id in b:
            pass
        else:
            print(print(file_id))
            print(file_id)
            file_id = file_id
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
            match_type = read_file['info']['event']['name']
            #match_type_number = read_file['info']['match_type_number']
            # winning_team_runs_lead = read_file['info']['outcome']['by']['runs']
            try:
                winning_team = read_file['info']['outcome']['winner']
            except:
                winning_team = read_file['info']['outcome']['result']
            team_type = read_file['info']['team_type']
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
            for innings in innings_details:
                total_score = 0
                innings_all_over = []
                overs = innings['overs']
                for over in overs:
                    each_over_score =0
                    overnumber = over['over']
                    over_number = over['over']
                    deliverirs = over['deliveries']
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
                    for delivery in deliverirs:
                        count +=1
                        runs_data = delivery['runs']
                        if int(runs_data['extras']) >0:
                            extras+=int(runs_data['extras'])
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
                    query = f"insert into cricket.eachball_data values({overnumber},{dot_ball},{ones},{twos},{threes},{fours},{sixes},{extras},{wickets},{each_over_score},{innings_count},'{file_id}')"
                    cur_name1.execute(query)
                    con_1.commit()
                    #delivery_keys=list(delivery.keys())
                    #
                    # delivery_details=[str(overs_count)+'.'+str(ball_count),delivery['batter'],delivery['non_striker'],delivery['bowler']
                    #                   ,[delivery['runs']['batter'],delivery['runs']['extras'],delivery['runs']['total']]]
                    # if 'extras' in delivery_keys:
                    #     extras_names =list(delivery['extras'].keys())
                    #     extras_details = [True,extras_names[0],delivery['extras'][extras_names[0]]]
                    # else:
                    #     extras_details = [False]
                    #delivery_details.append(extras_details)
                    each_over_score += int(delivery['runs']['total'])
                    total_score+= each_over_score
                    #over_details.append(delivery_details)
                    over['over_score']= each_over_score
                print(total_score)
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
                print(type(c_2))
                query = f"insert into cricket.season_details values('{season}','{home_team_name}','{away_team_name}','{date_details}','{match_type}','{players_gender}','{player_of_match}','{winning_team}','{toss_won_team}','{toss_dession}','{number_of_overs}'," \
                        f"'{team_type}','{stadium_name}','{innings_count}','{innings_all_over}',{total_score},'{file_id}');"
                cur_name1.execute(query)
                con_1.commit()
                #print(file_name)
                innings_count += 1
    return 'Completed'







def dump_data_into_db():
    dir_lists = sorted(os.listdir(r'C:\Users\User 101\Desktop\automation projects\cricket_scrape\ipl_json'))
    count = 0
    for i in dir_lists:
        get_file_data(i)
        count+=1
        if count ==100:
            break

# con_1.close()
dump_data_into_db()
# get_data_from_db()

