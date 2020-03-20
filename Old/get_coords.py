import requests
import json
from selenium import webdriver
import csv
from time import sleep
from datetime import date,timedelta
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import os
from reverse_geocoding import *

import urllib3
urllib3.disable_warnings()

progress_count = 0

#Bus id
# For SAM series : 272 + bus-number
# For ABP series : 666 + bus-number
# For ARR series : 509 + bus-number
# For ATP series : 717 + bus-number
# For CSR series : 523 + bus-number
# For SMD series : 761 + bus-number
# For SMT series : 804 + bus-number
# For TBO series : 848 + bus-number
# For TKR series : 507 + bus-number
# For ARM series : 355 + bus-number
# For CSM series : 376 + bus-number
# For TKM series : 361 + bus-number



#hours --> hours-6 (if -ve start reducing from 24)
# eg:
# 22 --> 16
# 5 --> 23

#minutes --> tens digit - 3 (if -ve start reducing from 6)
# eg: 
# 42 --> 12
# 22 --> 42


class CoordinateSearch:

    def __init__(self,cookie=None,bus_name="",interval=10,date=0,id=0):
        print('Search for {} started'.format(bus_name))
        if cookie is None:
            with open('cookies.log','r') as file:
                self.cookie = file.read()
        else:
            self.cookie = cookie

        self.progress = 0
        self.id = id
        
        self.ids = {'SAM':272,
        'ABP':666,
        'ARR':509,
        'ATP':717,
        'CSR':523,
        'SMD':761,
        'SMT':804,
        'TBO':848,
        'TKR':507,
        'ARM':355,
        'CSM':376,
        'TKM':361}

        self.date = date
        self.hour_counter = 8
        self.name = bus_name
        # self.id = self.get_id(bus_name)
        self.data_list = []
        # self.data_list.append(['Date','Time','Latitude','Longitude'])
        self.interval = interval
        self.data = {}
        self.cookies_arg = {'JSESSIONID':self.cookie}
        self.data_arg = {"type":"ASSET","ids":[self.id],"start":"2020-03-16T16:36:39.000Z","end":"2020-03-16T16:37:40.000Z","rtl":False}
        self.headers_arg = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
                    'Accept':'application/json, text/plain, */*',
                    'Accept-Language':'en-US,en;q=0.5',
                    'Accept-Encoding':'gzip, deflate',
                    'Content-Type':'application/json;charset=utf-8',
                    'Referer':'https://ajlavls.in/abpp/',
                    'Connection':'close',
                    'Origin':'https://ajlavls.in'}

    def change_args(self,**kwargs):
        # self.data_arg[kwargs.keys()[0]] = kwargs[kwargs.keys()[0]] 
        for key in kwargs.keys():
            self.data_arg[key] = kwargs[key]

    def get_cookie(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://ajlavls.in/abpp/#/login")
        sleep(3)
        self.driver.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div[2]/form/div[1]/input").send_keys('A_Yhonk')
        self.driver.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div[2]/form/div[2]/input").send_keys('A_Yhonk@123')
        self.driver.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div[2]/form/div[3]/div/input").click()
        sleep(3)
        cookies = self.driver.get_cookies()
        with open('cookies.log','w') as file:
            file.write(str(cookies[0]['value']))
        self.cookie = str(cookies[0]['value'])
        self.cookies_arg = {'JSESSIONID':self.cookie}
        self.driver.close()
        self.start()

    def get_id(self,name):
        # bus_number = int(name[3:])
        # bus_series = name[:3]
        # return (self.ids[bus_series] + bus_number)
        return 559

    def start(self):
        self.get_data(self.date,self.date,'08:00:00','08:01:00')

    def tune_data(self,date,time):
        start = date + "T"
        data = time.split(":")
        hour = int(data[0])
        minutes = data[1]
        seconds = str(data[2])
        
        tmp = hour - 6

        if tmp < 0:
            h = 24 + tmp
        else:
            h = tmp
        
        start += str(h)

        #Minutes
        tmp = int(minutes[0]) - 3

        if tmp < 0:
            h = 6 + tmp
        else:
            h = tmp
        h2 = str(h) + minutes[1]
        
        start += ':' + h2 + ':' + seconds + '.000Z'
        # print(start)
        return start

    def get_data(self,from_date,to_date,from_time,to_time):
        if self.hour_counter >= 20:
            return
        start = self.tune_data(from_date,from_time)
        end = self.tune_data(to_date,to_time)
        self.change_args(start=start,end=end)
        req = requests.post('https://ajlavls.in/abpp/rest/mrt',verify=False,data=json.dumps(self.data_arg),
                            headers=self.headers_arg,cookies=self.cookies_arg)
        
        if req.status_code == 405 or req.status_code == 400:
            self.get_cookie()
            return
        
        data = json.loads(req.text)
        try:
            longitude = data['assets'][str(self.id)]['logs'][0]['lon']
            latitude = data['assets'][str(self.id)]['logs'][0]['lat']

        except Exception as e:
            latitude = 0
            longitude = 0
            with open('logs.txt','a') as f:
                f.write(str(e) + '\n')

        self.data[from_date + " " + self.change(from_time)] = [latitude,longitude]
        self.data_list.append([from_date,self.change(from_time),latitude,longitude])
        self.progress += 1
        # print('{}% done'.format(str((self.progress/72)*100)[:4]))
        self.get_next(from_date,to_date,from_time,to_time)    

    def change(self,time):
        data = time.split(':')
        data[0] = str(self.hour_counter)
        return ':'.join(data)

    def get_next(self,from_date,to_date,from_time,to_time):
        data = from_time.split(":")
        hour = int(data[0])
        minutes = int(data[1])
        seconds = str(data[2])

        tmp = minutes + 10

        if tmp == 30:
            hour += 1
        if tmp >= 60:
            minutes = '00'
            self.hour_counter += 1
            from_time = str(hour) + ':' + '00' + ':' + str(seconds)
            to_time = str(hour) + ':' + '01' + ':' + str(seconds)
        else:
            minutes = tmp
            from_time = str(hour) + ':' + str(minutes) + ':' + str(seconds)
            to_time = str(hour) + ':' + str(int(minutes)+1) + ':' + str(seconds)
        
        self.get_data(from_date,to_date,from_time,to_time)

    def extract_data(self,List=False):
        if List:
            return self.data_list
        else:
            return self.data                                


# main = CoordinateSearch(cookie="01B23455F0C58D44BB3A9E09A17E1FB3",
#                         bus_name="ARR27",date="2020-03-17")

# main = CoordinateSearch(bus_name="ARR27",date="2020-03-17")
# main.start()

# with open('SAM8.csv','w') as f:
#     writer = csv.writer(f)
#     writer.writerows(main.extract_data(List=True))

def start(bus,id,dates):
    global progress_count
    main_data = []
    csv_data = [
        ['Date','Time','Latitude','Longitude']
    ]
    for date in dates:
        main = CoordinateSearch(bus_name=bus,date=date,id=id)
        main.start()
        main_data.append(main.extract_data(List=True))
    
    for i in main_data:
        for x in i:
            csv_data.append(x)
    
    # os.chdir('Data')
    with open('{}.csv'.format(bus),'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(csv_data)

    progress_count += 1
    print("[*] {}/100 buses done".format(str(progress_count)))

def main():
    thread_pool = ThreadPoolExecutor(max_workers=10)
    start_date = str(input("Please enter start date (YYYY-MM-DD) : ")).split('-')
    start_date = date(int(start_date[0]),int(start_date[1]),int(start_date[2]))
    end_date = str(input("Please enter end date (YYYY-MM-DD) : ")).split('-')
    end_date = date(int(end_date[0]),int(end_date[1]),int(end_date[2]))

    delta = end_date - start_date
    dates = []

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        dates.append(str(day))

    with open('buses.txt','r') as file:
        for line in file.readlines():
            data = line.split(',')
            thread_pool.submit(start,data[0],int(data[1]),dates)
            # search_thread = Thread(target=start,args=(data[0],int(data[1]),dates))
            # search_thread.start()
            # print('[*] Search for {} started'.format(data[0]))
            # search_thread.join()
    thread_pool.shutdown()

    


if __name__ == '__main__':
    main()


