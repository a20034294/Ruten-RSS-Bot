from selenium import webdriver
import time
import random
import re
import io


class Crawler():
    def __init__(self, driver):
        self.driver = driver
    def routine(self):
        driver = self.driver
        path = re.sub('crawler.py', '', __file__)
        path = path + './'

        db = {}
        queries = []
        try:
            with io.open(path + 'ruten.db', 'r') as f:
                for line in f.readlines():
                    clean_line = re.sub('\s', '', line)
                    db[clean_line] = 1
        except Exception:
            print('no Exist db')

        with io.open(path + 'query.db', 'r') as f:
            for line in f.readlines():
                clean_line = re.sub('\s', '', line)
                queries.append(clean_line)

        ban_flag = True
        send_content = 'Query Data:\n'

        for query in queries:
            if len(query) < 5 :
                continue
            print(query)
            driver.get(query)
            titles = driver.find_elements_by_xpath('//*[@id="ProdGridContainer"]/dl/dd/dl/dd/div/h5/a')
            for title in titles:
                ban_flag = False
                #if title.get_attribute('href') in db:
                #    continue
                print(title.get_attribute('innerHTML'))
                print(title.get_attribute('href'))
                #with io.open(path + 'ruten.db', 'a') as f:
                #    f.write(title.get_attribute('href') + '\n')
                send_content = send_content + title.get_attribute('innerHTML') + '\n' + title.get_attribute('href') + '\n\n'


        if ban_flag == True:
            print('baned');

        return send_content

    def query(self, query):
        driver = self.driver

        ban_flag = True
        send_content = 'Query Data:\n'

        if len(query) < 1 or len(query) > 30 :
            return send_content

        print(query)
        driver.get('https://find.ruten.com.tw/s/?area=0&platform=ruten&q=' + query + '&shipfee=all&sort=new%2Fdc')
        titles = driver.find_elements_by_xpath('//*[@id="ProdGridContainer"]/dl/dd/dl/dd/div/h5/a')
        for title in titles:
            if len(send_content) > 1500:
                break

            ban_flag = False

            print(title.get_attribute('innerHTML'))
            print(title.get_attribute('href'))
            send_content = send_content + title.get_attribute('innerHTML') + '\n' + title.get_attribute('href') + '\n\n'


        if ban_flag == True:
            print('baned');

        return send_content
