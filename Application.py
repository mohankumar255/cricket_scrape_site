from Fsb_Sites_checks.test1 import *
from flask import Flask, flash, send_from_directory,render_template,redirect,request
# import json, datetime, time
# from datetime import date, timedelta
from cricdb import *
import json
from flask_swagger_ui import get_swaggerui_blueprint
import requests, json

app = Flask(__name__)
app.secret_key = '\xfc\\%\xa5\xf6\x1c\xfe\xde".\xfc\xb32\xab\x8c\xbd\xf3\x89\tN6[\xca\xa9'
# server_name=''
# @app.route('/home', methods=['GET', 'POST'])
# @app.route('/', methods=['GET', 'POST'])

from Fsb_Sites_checks import Application
import Cricket_application

@app.route('/static/<path>')
def send_statics(path):
    return send_from_directory('static', path)


swagger_url = '/swagger_ui'
api_url = '/static/swagger.yml'
swagger_blueprint = get_swaggerui_blueprint(swagger_url, api_url,
                                            config={'app_name': 'python flask swagger connection'})
app.register_blueprint(swagger_blueprint, url_prefix=swagger_url)





# # @app.route('/home', methods=['GET', 'POST'])
# # def home_page():
# #     if request.method == 'POST':
# #        return render_template('filter.html', markets=markets, sports=sports, countrys_list=sorted(countries_list1),
# country_data=countrynames, countries=True, select_sport=[sport_name, sport_url], sport_select=is_sport_select)
# #     else:
# #        message='Please select valid sport'
# #        log_file(message)
# #        flash(message)
# #        return render_template('filter.html', markets=markets, select_sports=select_sports, sports=sports)
# #     return render_template('filter.html', markets=markets, sports=sports, select_sports=select_sports)


# @app.route('/submit_signup', methods=['GET', 'POST'])

#  @app.route('/signin', methods=['GET', 'POST'])


def signin_page():
    return render_template('main.html')


# @app.route('/submit_signin', methods=['GET', 'POST'])
def signin_submit():
    # print('signin_submit')
    session['logged_in'] = True
    # session['username'] = fn_signin_submit(request.form)
    return main()


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        flash('Logged out')
        return redirect('/login')

# @app.route('/Masters/<name>')


def menuitem_page(name):
    # print('menuitem_page(name)=', name)
    if name == "submit_signin":
        # print('--------- submit_signin')
        sign_status = set_signin(request.form)
        if sign_status:
            if 'support' in session['username']:
                return redirect('/fsb_checks')
            elif session['username'] =='mohan kumar':
                return redirect('/cricket')
            elif session ['username'] == 'gautham akula':
                return redirect('/matches')
            else:
                return redirect('/Matches')
        else:
            flash('Please enter correct credentials')
            return redirect('/login')
    elif name == "submit_signup":
        pass
    else:
        pass


@app.route('/')
def home_page():
    if 'username' in session:
        if 'support' in session['username']:
            return redirect('/fsb_checks')
        elif session['username'] == 'mohan kumar':
            return redirect('/cricket')
        elif session['username'] == 'gautham akula':
            return ('/matches')
    else:
        return redirect('/login')




@app.route('/api/sports')
def sports_api():
    sports_list12 = sports_list1()
    return json.dumps(sports_list12)



@app.route('/api/cricket/eachballdata/<matchid>/<from_over>/<to_over>',methods=['GET','POST'])
def get_each_ball_data(matchid,from_over,to_over):
    each_ball_data =get_eachball_details(matchid,int(from_over),int(to_over))
    return json.dumps(each_ball_data)



@app.route('/api/cricket/matchids/<season>',methods=['GET','POST'])
def send_all_matchids_into_api(season):
    season = season.replace('-','/')
    matchids = get_all_matchids(season)
    return json.dumps(matchids)


@app.route('/api/cricket/matches/<matchid>',methods=['GET','POST'])
def get_match(matchid):
    match_data = get_each_match(matchid)
    if match_data[-1]:
        return json.dumps(match_data)
    else:
        return json.dumps([{"message":'There are no matches'}])




@app.route('/api/cricket/seasons')
def send_all_seasons_list_to_api():
    all_seasons = get_all_seasons()
    return json.dumps(all_seasons)


@app.route('/api/cricket/<season>/all_matches')
def get_all_matches_in_api(season):
    get_matches = get_all_matches(season)
    return json.dumps(get_matches)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/checks/<site_id>')
def checks(site_id):
    return Application.checks(site_id)

# if session['username']=='mohan kumar':
app.add_url_rule('/fsb_matches_data','matches_list11',Application.get_matches_list)
app.add_url_rule('/cricket/players_list','players_list',Cricket_application.all_teams11,methods=['GET','POST'])
app.add_url_rule('/cricket_stats','cricket_stats',Cricket_application.cric_stats,methods=['GET','POST'])
app.add_url_rule('/fsb_checks','homedata',Application.home)
app.add_url_rule('/issues_details','Checks',Application.issues_details,methods=['GET', 'POST'])
app.add_url_rule('/add_details','add details',Application.add_details_function,methods=['GET', 'POST'])
app.add_url_rule('/check_site','checksite',Application.main, methods=['GET', 'POST'])
app.add_url_rule("/cricket", 'Cricket', Cricket_application.cricket_home_data, methods=['GET', 'POST'])
app.add_url_rule("/statcenter", "", main)
app.add_url_rule("/home", "home", main)
# app.add_url_rule("/signup", "signup", signup_page)
app.add_url_rule("/submit_signup", "submit_signup", signup_submit)
# app.add_url_rule("/signin", "signin", signin_page)
app.add_url_rule("/submit_signin", "submit_signin", signin_submit)
app.add_url_rule("/<name>", "menuitem_page", menuitem_page, methods=['GET', 'POST'])
# app.add_url_rule('/league_scrape/<id>', league_scrape, methods=['Get', 'POST'])
# app.add_url_rule('/country_scrape/<name>', country_scrape, methods=['Get', 'POST'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=False)
