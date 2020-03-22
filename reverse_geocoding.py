import requests
import json
from datetime import date,datetime
from time import sleep
# from get_coords import log

def log(a):
    pass

#Key1 : 0ed244a8d1cf03  (deveshthechamp@gmail.com)
#Key2 : 10ccca1e377cbf (moneyexperts99@gmail.com)
#Key3 : e70d408d0bfdea (devesh.cok@gmail.com)
#Key4 : fbe5313055ae5b (deveshthetube@gmail.com)

keys_main = ['0ed244a8d1cf03','10ccca1e377cbf','e70d408d0bfdea','fbe5313055ae5b']
keys = ['0ed244a8d1cf03','10ccca1e377cbf','e70d408d0bfdea','fbe5313055ae5b']

def get_area(lat,lon,key=0,set=1):
    global keys,keys_main
    # if set == 1:
    #     keys = keys[:2]
    # elif set == 2:
    #     keys = keys[2:]
    try:
        url = "https://us1.locationiq.com/v1/reverse.php"

        data = {
            'key': keys[key],
            'lat': str(lat),
            'lon': str(lon),
            'format': 'json'
        }
        log('Requesting area data')
        response = requests.get(url, params=data,timeout=10)
        log('Area data received')
        data = json.loads(response.text)
        return data['display_name']
    except IndexError:
        print('[*] API limit exceeded')
    except Exception as e:
        # print('[*] Switiching API keys...')
        log('Exception occurred')

        if data['error'] == "Rate Limited Day":
            keys.remove(keys[key])
        elif data['error'] == "Rate Limited Minute":
            log('Sleeping...')
            sleep(30)
        
        with open('errors.log','a') as file:
            meta_data = str(date.today()) + "  " + datetime.now().time().strftime("%H:%M:%S") + "  " + ':' + "  "
            file.write(meta_data + str(e) + " " + response.text +  '\n')
        log('Switching to key {}'.format(str(key+1)))
        # get_area(lat,lon,key=key+1)
        log('Using key {}'.format(str(keys_main.index(keys[0]))))
        return get_area(lat,lon)

def get_balance(key):
    url = "https://us1.locationiq.com/v1/balance.php"

    data = {
        'key': key
    }

    response = requests.get(url, params=data)
    data = json.loads(response.text)
    return int(data['balance']['day'])

# print(get_area(23,72))