import datetime
import json
from psycopg2 import pool

SANhost = '192.168.2.94'
SANdb = 'sportsit_db'
DataCenterhost = '192.168.2.94'
DataCenterdb = 'datacenter'
dbuser = 'postgres'
dbpwd = 'root'
connection_pool_1 = pool.SimpleConnectionPool(1,10,host=SANhost, database=DataCenterdb, user=dbuser, password=dbpwd)
con_1=connection_pool_1.getconn()
cur_name1 = con_1.cursor()

def get_issues_details():
    query = 'select * from "FsbSiteChecks".issues_details'
    cur_name1.execute(query)
    fetch_data = cur_name1.fetchall()
    data = []
    for data_values in fetch_data:
        data.append([data_values[0],data_values[1],data_values[2]])
    return data

def get_all_existed_ids():
    all_ids = []
    query = 'select * from "FsbSiteChecks".issues_details'
    cur_name1.execute(query)
    fetch_data = cur_name1.fetchall()
    for data_values in fetch_data:
        all_ids.append(int(data_values[0]))
    return all_ids


def update_details(id ,title,description,insert_name,reason):
    print(title)
    query = f'update "FsbSiteChecks".issues_details set'+f" title='{title}' , description='{description}',insert_name='{insert_name}',reason='{reason}',inserted_date='{datetime.datetime.now()}' where s_id={id}"
    cur_name1.execute(query)
    con_1.commit()

def delete_record(id):
    query = f'delete from "FsbSiteChecks".issues_details where s_id={id}'
    cur_name1.execute(query)
    return 'Record deleted'

def add_details(id ,title,description):
    query = f'insert into "FsbSiteChecks".issues_details values'+f"({id},'{title}','{description}')"
    cur_name1.execute(query)
    con_1.commit()

def get_menus():
    query = 'select * from "FsbSiteChecks".menus where is_live=1'
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    return fetc
def get_submenus(menuid):
    query = f'SELECT submenuid,"Name" FROM "FsbSiteChecks"."Submenus" where menuid = {menuid}'
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    return fetc

def get_all_submenus_list():
    query = f'SELECT * FROM "FsbSiteChecks"."Submenus"'
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    return fetc

    
def get_all_menus():
    menus_list = [['All',[['Mobile_sites','Mobile_sites'],['Opera_sites','Opera_sites']]]]
    menus = get_menus()
    for i in menus:
        submenus_list = []
        submenus= get_submenus(i[1])
        for j in submenus:
            submenus_list.append(j)
        menus_list.append([i[0],submenus])
    return menus_list

def get_functions():
    query = 'select * from "FsbSiteChecks".functionalities'
    cur_name1.execute(query)
    fetc = cur_name1.fetchall()
    return fetc

#con_1.close()
