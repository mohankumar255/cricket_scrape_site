import json,requests
market_names=[[1,'1x2'],[2,'12'],[4,'1_2'],[6,'moneyline'],[7,'matchresult_ot']]

def live_now_api_data(url,sportid):
    count = 0
    sportid=int(sportid)
    if 'betlion' in url:
        print(market_names)
        for i in market_names:
            print(i)
            if i[0]== sportid:
                print(i[0],i[1])
                live_now_api=f'http://172.16.3.6/api/LiveNOWAPI/{sportid}/{i[1]}/null'
                res=requests.get(live_now_api)
                json_data=res.json()
                a=json_data[0]['leagues']

                for i in a:
                    b=i['events']
                    count+=len(b)
    return count


print(live_now_api_data('betlion',7))