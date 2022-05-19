import time

from flask import Flask
from Cricket_application import *
from Fsb_Sites_checks.test1 import *
from Fsb_Sites_checks import Application
from check_all_sites import application
from automated_scripts.fsb_sites import run_fsb_sites
from automated_scripts.tenbet_sites import check_site
from check_all_sites.tencric import  check_site as tencric_site_check

app = Flask(__name__)
app.secret_key = '\xfc\\%\xa5\xf6\x1c\xfe\xde".\xfc\xb32\xab\x8c\xbd\xf3\x89\tN6[\xca\xa9'


import threading

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

submenus = [['10bet tz',url1,5,userid_1,password_1,1],['M.10bet tz',url1_opera,5,userid_1,password_1,2],['10bet gh',url2,5,userid_2,password_2,3],['M.10bet gh',url2_opera,5,userid_2,password_2,4],['10bet zm',url3,5,userid_3,password_3,5]
            ,['M.10bet zm',url3_opera,5,userid_3,password_3,6],['10bet drc',url4,5,userid_4,password_4,7],['M.10bet drc',url4_opera,5,userid_4,password_4,8]]

mobile_sites = [submenus[0],submenus[2],submenus[4],submenus[6]]
opera_sites = [submenus[1],submenus[3],submenus[5],submenus[7]]



def tenbet_sites_running():
    threding_append = []
    for i in range(len(mobile_sites)):
        threding_append.append(threading.Thread(target=check_site, args=(
        mobile_sites[i][1], mobile_sites[i][3], mobile_sites[i][4], mobile_sites[i][2],
        mobile_sites[i][0],)))
    # check_site('https://10bet.co.tz/login?overrideregion=true',765765765,1234,5,'10bet TZ site')
    for i in threding_append:
        i.start()
    for j in threding_append:
        j.join()
    time.sleep(3)
    threding_append = []
    for i in range(len(opera_sites)):
        threding_append.append(threading.Thread(target=check_site, args=(
        opera_sites[i][1], opera_sites[i][3], opera_sites[i][4], opera_sites[i][2],
        opera_sites[i][0],)))
    # check_site('https://10bet.co.tz/login?overrideregion=true',765765765,1234,5,'10bet TZ site')
    for i in threding_append:
        i.start()
    for j in threding_append:
        j.join()
    time.sleep(3)


@app.route('/api/cricket/<season>/all_matches')
def get_all_matches_in_api(season):
    get_matches = get_all_matches(season)
    return json.dumps(get_matches)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        flash('Logged out')
        return redirect('/login')


@app.route('/', methods=['GET', 'POST'])
def redirect_method():
    if 'username' in session:
        if 'support' in session['username']:
            return redirect('/t_bet_sites')
        else:
            return redirect('/cricket')
    else:
        return redirect('/login')


@app.route('/login')
def login():
    return render_template('SignIn.html')


@app.route('/api/cricket/matches/<matchid>', methods=['GET', 'POST'])
def get_match(matchid):
    match_data = get_each_match(matchid)
    if match_data[-1]:
        return json.dumps(match_data)
    else:
        return json.dumps([{"message": 'There are no matches'}])


@app.route('/submit_signin', methods=['GET', 'POST'])
def submit_signin():
    if request.method == 'POST':
        sign_status = set_signin(request.form)
        if sign_status[0]:
            session['username'] = sign_status[1]
            if 'support' in session['username']:
                return redirect('/fsb_checks')
            elif session['username'] == 'mohan kumar':
                return redirect('/cricket')
        else:
            flash('Please anter correct credentials')
            return redirect('/login')


@app.route('/api/cricket/seasons')
def send_all_seasons_list_to_api():
    all_seasons = get_all_seasons()
    return json.dumps(all_seasons)


@app.route('/checks/<site_id>')
def checks(site_id):
    return Application.checks(site_id)

@app.route('/t_bet_checks/<site_id>')
def ten_bet_checks(site_id):
    return application.checks(site_id)



@app.route('/api/cricket/matchids/<season>', methods=['GET', 'POST'])
def send_all_matchids_into_api(season):
    season = season.replace('-', '/')
    matchids = get_all_matchids(season)
    return json.dumps(matchids)


@app.route('/api/cricket/eachballdata/<matchid>/<from_over>/<to_over>', methods=['GET', 'POST'])
def get_each_ball_data(matchid, from_over, to_over):
    each_ball_data = get_eachball_details(matchid, int(from_over), int(to_over))
    return json.dumps(each_ball_data)



from Fsb_Sites_checks.fsb_db import *

def edit_details(id):
    #if request.method=='POST':
        #id = request.form.get('id')
    data1 = get_issues_details()
    for data in data1:
        if data[0] == int(id):
            values = data
            break
    return render_template('edit_page.html',data =values)


def delete_records(id):

    delete_record(int(id))
    flash('Record Deleted')
    return redirect('/issues_details')


def update_data():
    if request.method == 'POST':
        id = int(request.form.get('id'))
        title = request.form.get('title')
        description = request.form.get('description')
        insert_name = request.form.get('insert_name')
        reason = request.form.get('reason')
        update_details(id,title,description,insert_name,reason)
        flash('Data updated')
    return redirect('/issues_details')


def run_auto_fsb_sites():
    while True:
        run_fsb_sites()
        time.sleep(300)

def run_10bet_sites():
       while True:
        tenbet_sites_running()
        time.sleep(300)


def run_10cric_site():
    while True:
        tencric_site_check('10cric','https://www.10cric.com/','TestUserSong04',123456,7)
        time.sleep(300)


def all_sites_run():
    while True:
        run_fsb_sites()
        time.sleep(5)
        tenbet_sites_running()
        time.sleep(5)
        tencric_site_check('10cric','https://www.10cric.com/','TestUserSong04',123456,7)
        time.sleep(300)


app.add_url_rule("/All_sites_run", 'All sites', all_sites_run, methods=['GET', 'POST'])
app.add_url_rule("/run_10cric_site", '10cric site', run_10cric_site, methods=['GET', 'POST'])
app.add_url_rule("/run_fsb_sites", 'Fsb sites', run_auto_fsb_sites, methods=['GET', 'POST'])
app.add_url_rule('/run_10bet_sites', '10bet sites', run_10bet_sites, methods=['GET', 'POST'])
app.add_url_rule("/cricket", 'Cricket', cricket_home_data, methods=['GET', 'POST'])
app.add_url_rule('/cricket/players_list', 'players_list', all_teams11, methods=['GET', 'POST'])
app.add_url_rule('/cricket_stats', 'cricket_stats', cric_stats, methods=['GET', 'POST'])
app.add_url_rule('/update_details', 'update data', update_data, methods=['GET', 'POST'])
app.add_url_rule("/edit_details/<id>", 'edit_details', edit_details, methods=['GET', 'POST'])
app.add_url_rule('/fsb_details', 'details', Application.issues_details,methods=['GET', 'POST'])
app.add_url_rule('/fsb_matches_data', 'matches_list11', Application.get_matches_list,methods=['GET', 'POST'])
app.add_url_rule('/delete_record/<id>', 'delete record', delete_records, methods=['GET', 'POST'])
app.add_url_rule('/t_bet_sites','10betsites',application.home,methods=['GET','POST'])
app.add_url_rule('/fsb_checks', 'homedata', Application.home, methods=['GET', 'POST'])
app.add_url_rule('/issues_details', 'Checks', Application.issues_details, methods=['GET', 'POST'])
app.add_url_rule('/add_details', 'add details', Application.add_details_function,methods=['GET', 'POST'])
app.add_url_rule('/check_site', 'checksite', Application.main, methods=['GET', 'POST'])
app.add_url_rule('/t_bet_check_site', '10betchecksite', application.main, methods=['GET', 'POST'])
