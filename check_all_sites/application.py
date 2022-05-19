import json,time,datetime
# from Fsb_Sites_checks.comman_use_libraries import *
import concurrent.futures
from flask import render_template, request, redirect, flash, session
from Fsb_Sites_checks.fsb_db import *
from check_all_sites.tenbet_sites import check_site


url1 = 'https://10bet.co.tz/login?overrideregion=true'
url2 = 'https://10bet.com.gh/login?overrideregion=true'
url3 = 'https://10bet.co.zm/login?overrideregion=true'
url4 = 'https://10betdrc.com/login?overrideregion=true'

url1_opera = 'https://m.10bet.co.tz/login?overrideregion=true'
url2_opera = 'https://m.10bet.com.gh/login?overrideregion=true'
url3_opera = 'https://m.10bet.co.zm/login?overrideregion=true'
url4_opera = 'https://m.10betdrc.com/login?overrideregion=true'

userid_1 = 765765765
password_1 = 1234

userid_2 = 245245245
password_2 = 1234

userid_3 = 962962962
password_3 = 1234

userid_4 = 840840840
password_4 = 1234



menus = [['All',[['Mobile_sites','Mobile Sites'],['Opera_sites','Opera Sites']]],['10Bet Tz',[[1,'Mobile site'],[2,'Opera_site']]],['10Bet Ghana',[[3,'Mobile site'],[4,'Opera_site']]],['10Bet ZM',[[5,'Mobile site'],[6,'Opera_site']]],['10Bet DRC',[[7,'Mobile site'],[8,'Opera_site']]]]
submenus = [['10bet tz',url1,5,userid_1,password_1,1],['M.10bet tz',url1_opera,5,userid_1,password_1,2],['10bet gh',url2,5,userid_2,password_2,3],['M.10bet gh',url2_opera,5,userid_2,password_2,4],['10bet zm',url3,5,userid_3,password_3,5]
            ,['M.10bet zm',url3_opera,5,userid_3,password_3,6],['10bet drc',url4,5,userid_4,password_4,7],['M.10bet drc',url4_opera,5,userid_4,password_4,8]]


mobile_sites = [submenus[0],submenus[2],submenus[4],submenus[6]]
opera_sites = [submenus[1],submenus[3],submenus[5],submenus[7]]

# app=Flask(__name__)
# app.secret_key='\xfc\\%\xa5\xf6\x1c\xfe\xde".\xfc\xb32\xab\x8c\xbd\xf3\x89\tN6[\xca\xa9'

def all_mobile_site_checks(filters,i):
    mobile_sites[i].append(filters)
    submenus_ids = mobile_sites
    result = check_site(submenus_ids[i][0],submenus_ids[i][1],submenus_ids[i][2],submenus_ids[i][3],submenus_ids[i][4],submenus_ids[i][6])
    return [submenus_ids[i][0],result]

def all_opera_site_checks(filters, i):
    opera_sites[i].append(filters)
    submenus_ids = opera_sites
    result = check_site(submenus_ids[i][0], submenus_ids[i][1], submenus_ids[i][2],
                        submenus_ids[i][3], submenus_ids[i][4], submenus_ids[i][6])
    return [submenus_ids[i][0],result]


def all_2(filters):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(all_opera_site_checks, filters,i) for i in range(len(opera_sites))]
        d = []
        for f in concurrent.futures.as_completed(results):
            d.append(f.result())
    # results = [executor.submit(all_sites_checks, i) for i in range(len(values1), len(values3))]
    return d


def all_1(filters):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(all_mobile_site_checks, filters,i) for i in range(len(mobile_sites))]
        d = []
        for f in concurrent.futures.as_completed(results):
            d.append(f.result())
    # results = [executor.submit(all_sites_checks, i) for i in range(len(values1), len(values3))]
    return d


def main():
    id1 = request.form.get('site_id')
    functions_checks_list = request.form.getlist('functions')
    functins_filters = []
    for i in functions_checks_list:
        functins_filters.append(int(i))
    message = ''
    title = ''
    date_time = datetime.datetime.fromtimestamp(time.time())
    if id1 == 'Mobile_sites':
        message = all_1(functins_filters)
    elif id1 == 'Opera_sites':
        message = all_2(functins_filters)
    else:
        id = int(id1)
        print('============')
        print(id)
        for details in submenus:
            if details[5] == id:
                data_details = details
                title = data_details[0]
                id = id-1
                submenus[id].append(functins_filters)

                message = check_site(submenus[id][0],submenus[id][1],submenus[id][2],submenus[id][3],submenus[id][4],submenus[id][6])
                #message = each_site_check(id, title, functins_filters)
                message = [[title, message]]
    return render_template('t_bet_base.html', messages=message, list_items=menus,
                           show_messages=True, executed_time=date_time)


def checks(site_id):
    if site_id == 'Mobile_sites':
        title = 'Mobile Sites'
    elif site_id == 'Opera_sites':
        title = 'Opera sites'
    elif site_id == 'details':
        return redirect('/issues_details')
    else:
        for details in submenus:
            if details[5] == int(site_id):
                data_details = details
                break
        title = data_details[0]
    functions_list = get_functions()
    return render_template('t_bet_functions.html', functions_list=functions_list,
                           site_id=site_id, site_name=title)


def home():
    if 'username' in session:
        nums1 = [1, 2, 3, 4]
        return render_template('t_bet_base.html', list_items=menus, show_messages=False,
                               nums=nums1)

    else:
        return redirect('/login')
