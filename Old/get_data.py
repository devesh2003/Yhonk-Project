from selenium import webdriver
from time import sleep

class GetCoordinates:

    #Coordinates --> Dictionary (Key: Time,Value: List pair of latitude and longitude)

    def __init__(self,bus_name,interval=10,creds=[],from_date=0,to_date=0):
        self.name = bus_name
        self.interval = interval
        self.username = creds[0]
        self.passwd = creds[1]
        self.coordinates = {}
        self.from_date = from_date
        self.to_date = to_date
        self.driver = webdriver.Chrome()
        self.login()

    def login(self):
        self.driver.get("https://ajlavls.in/abpp/#/login")
        sleep(3)
        self.driver.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div[2]/form/div[1]/input").send_keys(self.username)
        self.driver.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div[2]/form/div[2]/input").send_keys(self.passwd)
        self.driver.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div[2]/form/div[3]/div/input").click()
        sleep(2)
        self.driver.get('https://ajlavls.in/abpp/#/mrt')
        sleep(5)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/mrt-player/div/mrt-player-header/mrt-loader/div/div/button').click()
        sleep(4)
        from_date = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/mrt-player/div/mrt-player-header/mrt-loader/div[2]/div[2]/mrt-loader-asset/form/div[2]/div/div/input')
        to_date = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/mrt-player/div/mrt-player-header/mrt-loader/div[2]/div[2]/mrt-loader-asset/form/div[3]/div/div/input')
        from_time = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/mrt-player/div/mrt-player-header/mrt-loader/div[2]/div[2]/mrt-loader-asset/form/div[2]/div/input')
        to_time = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/mrt-player/div/mrt-player-header/mrt-loader/div[2]/div[2]/mrt-loader-asset/form/div[3]/div/input')
        from_date.clear()
        to_date.clear()
        to_time.clear()
        from_time.clear()
        from_date.send_keys(self.from_date)
        to_date.send_keys(self.to_date)
        from_time.send_keys('08:00:00')
        to_time.send_keys('08:01:00')
        to_time.clear()
        to_time.send_keys('08:01:00')
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/mrt-player/div/mrt-player-header/mrt-loader/div[2]/div[2]/mrt-loader-asset/form/div[1]/div/div[1]/input').send_keys(self.name)
        sleep(2)
        self.driver.find_element_by_id('ui-select-choices-row-1-0').click()
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/mrt-player/div/mrt-player-header/mrt-loader/div[2]/div[2]/mrt-loader-asset/form/div[5]/button').click()
        sleep(500)

    def set_time(self):
        pass

    def increment_time(self):
        pass

    def get_coords(self):
        pass


GetCoordinates('SAM8',creds=['A_Yhonk','A_Yhonk@123'],from_date='2020-03-16',to_date='2020-03-16')