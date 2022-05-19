from cricdb import *
import requests
from flask import render_template, request, flash, session, redirect
from cricket_apis import *


def eachover_count(matchid, from_over, to_over):
    eachball_details = get_eachball_data_from_api(matchid, from_over, to_over)
    l1 = []
    row_values = [x for x in range(6)]
    column_values = [0, 1, 2, 3, 4, 6, 'other']
    for i in range(6):
        l2 = []
        l2.append(i)
        for j in range(7):
            count = 0
            for ball_count in eachball_details:
                if ball_count[j + 1] == i:
                    count += 1
            l2.append(count)
        l1.append(l2)
    percentage_values = []
    count = 0
    for i in l1:
        l2 = []
        l2.append(count)
        count += 1
        for j in i[1:]:
            l2.append(float("{0:.1f}".format((j / len(eachball_details)) * 100)))
        percentage_values.append(l2)
    decimal_values = []
    count = 0
    for i in percentage_values:
        l2 = []
        l2.append(count)
        count += 1
        for j in i[1:]:
            if int(j) == 0:
                l2.append(0)
            else:
                l2.append(float("{0:.1f}".format((1 / j) * 100)))
        decimal_values.append(l2)
    print(percentage_values)
    return [l1, percentage_values, decimal_values, row_values, column_values, len(eachball_details)]


def cric_stats():
    data = {}
    data["players_stats"] = False
    data['stats'] = []
    home_team = 'All'
    away_team = 'All'
    get_all_teams_list = get_all_teams()
    if request.method == 'POST':
        home_team = request.form.get('home_team')
        away_team = request.form.get('away_team')
        if home_team != 'All':
            if away_team != 'All':
                if home_team != away_team:
                    get_stats = cric_stats_center(home_team, away_team)
                    home_team_players = teams_players_list(home_team)
                    away_team_players = teams_players_list(away_team)
                    home_team_players_ids = list(map(lambda x: x[1], home_team_players))
                    away_team_players_ids = list(map(lambda x: x[1], away_team_players))
                    data['home_team_players'] = home_team_players
                    data['away_team_players'] = away_team_players
                    data['players_stats'] = True
                    data['stats'] = get_stats[0]
                    data['home_win_count'] = get_stats[1]
                    data['away_win_count'] = get_stats[2]
                    data['home_players_rating_data'] = players_rating(home_team_players_ids)
                    data['away_team_rating_data'] = players_rating(away_team_players_ids)
                    data['home_team_players'] = home_team_players
                    data['away_team_players'] = away_team_players
                    data['players_stats_data'] = compare_batters_data(home_team_players_ids,
                                                                      away_team_players_ids)
    return render_template('crcistats.html', cricket_stats_is_show=True, data=data,
                           get_all_teams_list=get_all_teams_list, home_team=home_team,
                           away_team=away_team)


def all_teams11():
    teams_list = sorted(get_all_teams())
    a1 = []
    for i in range(len(teams_list)):
        a1.append([i, teams_list[i]])
    all_players = players_list11()
    data1 = {}
    data1['teams'] = a1
    data1['players'] = all_players
    if request.method == 'POST':
        players_list1 = list(request.form.getlist('players1'))
        team_id = request.form.get('team')
        print(team_id)
        team_name = teams_list[int(team_id)]
        print(team_name)
        for id in players_list1:
            add_player(id, int(team_id), team_name)
    return render_template('players_select_list.html', data1=data1)


def cricket_home_data():
    seasons = get_all_seasons_from_api()
    home_teams = ''
    home_team = 'All'
    away_team = 'All'
    away_teams = ''
    each_over_data = ''
    seasons_data = ''
    kickoff = ''
    matcheid = ''
    matchdata = []
    for i in range(20):
        matchdata.append(i)
    is_select_season = False
    is_select_home_team = False
    is_select_away_team = False
    select_home_team = ''
    select_away_team = ''
    season_name = ''
    is_select_sport = False
    each_ball_data = ''
    from_over = 1
    to_over = 40
    matchid_key = ''
    batters_data = ''
    bowler_data = ''
    select_sport_details = ['Cricket', 3]
    seasons_matches_data = ['', '']
    if request.method == 'POST':
        sport_id = request.form.get('dd_sport')
        print(sport_id)
        if sport_id != '3' and 'username' not in session:
            return redirect('/login')
        is_select_sport = True
        sport_name = 'Cricket'
        season_name = request.form.get('seasons')
        print(season_name)
        if season_name:
            if season_name != 'All':
                is_select_season = True
                seasons_matches_data = []
                matcheids = get_all_matchids_from_api(season_name)
                # for matcheid in matcheids:
                #     matchdata = get_match_data_from_api(matcheid)
                #     if matchdata[-1]:
                #         each_ball_data = get_eachball_data_from_api(matcheid, 1, 40)
                #         seasons_matches_data.append([matchdata,[matchdata[4],matchdata[5]],matcheid,each_ball_data])
                seasons_matches_data = get_all_matches(season_name)
                home_teams = all_home_teams(season_name)
                home_team = request.form.get('home_team')
                if home_team:
                    if home_team != 'All':
                        over_from_1 = request.form.get('over_from')
                        over_to_1 = request.form.get('over_to')
                        away_team = request.form.get('away_team')
                        is_select_home_team = True
                        select_home_team = home_team
                        away_teams = all_away_teams(season_name, home_team)
                        if away_team:
                            if away_team != 'All':
                                is_select_away_team = True
                                select_away_team = away_team
                                if over_from_1:
                                    from_over = int(over_from_1)
                                if over_to_1:
                                    to_over = int(over_to_1)
                                match_data = all_data(season_name, home_team, away_team)
                                if match_data[-1]:
                                    matchid = match_data[3]
                                    batters_data = get_batter_data(matchid)
                                    bowler_data = get_bowler_data(matchid)
                                    matchdata = get_match_data_from_api(matchid)
                                    each_over_data = eachover_count(matchid, from_over, to_over)
                                    each_ball_data = get_eachball_data_from_api(matchid, from_over,
                                                                                to_over)
                                    if from_over >= to_over or from_over == to_over:
                                        flash('Please select correct over range')
                                    # to avoid collapse id dulipcate add extra value to matchid
                                    matchid_key = str(matchid) + 'xyz'
                                    individual_match_data = matchdata
                                else:
                                    matchdata = ['1', '2', '3']
                                    print("Please contact admin")
                                    is_select_away_team = False

    return render_template('cric_home_page.html', bowler_data=bowler_data,
                           batters_data=batters_data, each_over_data=each_over_data,
                           from_over=from_over, to_over=to_over, cricket_sport=True,
                           seasons=seasons, season_name=season_name,
                           home_teams=home_teams, away_teams=away_teams,
                           is_select_season=is_select_season,
                           is_home_team_select=is_select_home_team
                           , is_select_away_team=is_select_away_team,
                           data=[matchdata, [matchdata[4], matchdata[5]], matcheid],
                           feeds_data=[matchdata[4], matchdata[5]],
                           select_home_team=select_home_team, select_away_team=select_away_team,
                           seasons_matches_data=seasons_matches_data,
                           is_select_sport=is_select_sport,
                           select_sport_details=select_sport_details, each_ball_data=each_ball_data,
                           dict1={'name': "mohankumar"}, select_match_id=matchid_key)
