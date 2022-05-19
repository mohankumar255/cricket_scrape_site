# import json,time,datetime
# from Fsb_Sites_checks.comman_use_libraries import *
from Fsb_Sites_checks.test1 import *
import concurrent.futures
from flask import render_template, request, redirect, flash, session
from Fsb_Sites_checks.betlion_login import site_checks
from Fsb_Sites_checks.fsb_db import *

# app=Flask(__name__)
# app.secret_key='\xfc\\%\xa5\xf6\x1c\xfe\xde".\xfc\xb32\xab\x8c\xbd\xf3\x89\tN6[\xca\xa9'
all_menus_list = get_all_menus()


all_submenus_details = get_all_submenus_list()
print(all_menus_list)

print(all_submenus_details)

mobile_sites = []
opera_sites = []
for site in all_submenus_details:
    if '//m.' in site[1]:
        opera_sites.append(site)
    else:
        mobile_sites.append(site)


def each_site_check(id, site_name, filters):
    for details in all_submenus_details:
        if details[5] == int(id):
            data_details = details
            a = site_checks(site_name, data_details[1], data_details[3], data_details[4], data_details[2],
                    filters)
            return a




def all_sites_checks(id, filters):
    if True:
        data_details = mobile_sites[id]
        a = site_checks(data_details[0], data_details[1], data_details[3], data_details[4],
                        data_details[2], filters)
    # except Exception as error:
    #     print(error)
    #     log_file(str(error))
    #     a=[['error occured',False]]
    print(data_details)
    return [data_details[0], a]


def all_1(filters):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(all_sites_checks, i, filters) for i in range(len(mobile_sites))]
        d = []
        for f in concurrent.futures.as_completed(results):
            d.append(f.result())
    # results = [executor.submit(all_sites_checks, i) for i in range(len(values1), len(values3))]
    return d


def all_2(filters):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(all_sites_checks, i, filters) for i in range(len(opera_sites))]
        d = []
        for f in concurrent.futures.as_completed(results):
            d.append(f.result())
    # results = [executor.submit(all_sites_checks, i) for i in range(len(values1), len(values3))]
    return d


def all(filters):
    a = all_1(filters)
    # b=all_2(filters)
    # c=a+b
    return a


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
        for details in all_submenus_details:
            if details[5] == id:
                data_details = details
                title = data_details[0]
                message = each_site_check(id, title, functins_filters)
                message = [[title, message]]

    return render_template('fsb_base.html', messages=message, list_items=all_menus_list,
                           show_messages=True, executed_time=date_time)


def get_matches_list():
    get_matches_data = get_data()
    print(get_matches_data)
    return render_template('fsb_base.html', matches_count=True,
                           get_matches_data=get_matches_data[0], list_items=all_menus_list,
                           total_counts=get_matches_data[1])


def checks(site_id):
    print(site_id)
    print('==============')
    print(site_id)
    if site_id == 'Mobile_sites':
        title = 'Mobile Sites'
    elif site_id == 'Opera_sites':
        title = 'Opera sites'
    elif site_id == 'details':
        return redirect('/issues_details')
    else:
        for details in all_submenus_details:
            if details[5] == int(site_id):
                data_details = details
                break
        title = data_details[0]
    functions_list = get_functions()
    return render_template('fsb_select_checks_page.html', functions_list=functions_list,
                           site_id=site_id, site_name=title)


def home():
    if 'username' in session:

        nums1 = [1, 2, 3, 4]
        return render_template('fsb_base.html', list_items=all_menus_list, show_messages=False,
                               nums=nums1)
    else:
        return redirect('/login')


def issues_details():
    return render_template('fsb_issues_details.html', issues_details_data=get_issues_details(),
                           list_items=all_menus_list)


def add_details_function():
    if request.method == 'POST':
        get_ids = get_all_existed_ids()
        for i in range(100000):
            if i in get_ids:
                pass
            else:
                id = i
                break
        title = request.form.get('title')
        description = request.form.get('description')
        if len(description) > 10:
            add_details_data = add_details(int(id), title, description)
            flash("Data added")
        return redirect('/issues_details')
