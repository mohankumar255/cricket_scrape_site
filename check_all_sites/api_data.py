import requests
import datetime


def get_feed_data(feed):
    respons_code = feed['statusCode']
    event_ids = []
    if respons_code == 100:
        fixtures_count = feed['result']['fixtures']
        matches_count = len(fixtures_count)
        for i in fixtures_count:
            event_ids.append(i['fixtureId'])
    return [matches_count, event_ids]

def live_now_api(sport_id):
    client_id = '244F1375-7BC3-48D9-66F9-08D94057C6CB'
    api_key = '8LKvrh6C2fe8mKXZ'
    headers={'x-client-id':client_id,
             'x-api-key':api_key}
    url=f'https://prod-af-platformapi.song88.com/v1/sportsbook/sports/livefixtures?sportId={sport_id}'
    resp=requests.get(url,headers=headers)
    json_data=resp.json()
    return get_feed_data(json_data)

#print(live_now_api(20))


def today_feed(sport_id):
    url = f'https://prod-af-platformapi.song88.com/v1/sportsbook/sports/todayfixtures?sportId={sport_id}'
    client_id = '244F1375-7BC3-48D9-66F9-08D94057C6CB'
    api_key = '8LKvrh6C2fe8mKXZ'
    headers={'x-client-id':client_id,
             'x-api-key':api_key}
    resp=requests.get(url,headers=headers)
    json_data=resp.json()
    return get_feed_data(json_data)