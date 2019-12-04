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
        email_content = 'Query Data:\n'

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
                with io.open(path + 'ruten.db', 'a') as f:
                    f.write(title.get_attribute('href') + '\n')
                    email_content = email_content + title.get_attribute('innerHTML') + '\n' + title.get_attribute('href') + '\n\n'


        if ban_flag == True:
            print('baned');

        return email_content

    def query(self, query):
        driver = self.driver

        ban_flag = True
        email_content = 'Query Data:\n'

        if len(query) < 5 :
            return email_content

        print(query)
        driver.get(query)
        titles = driver.find_elements_by_xpath('//*[@id="ProdGridContainer"]/dl/dd/dl/dd/div/h5/a')
        for title in titles:
            ban_flag = False

            print(title.get_attribute('innerHTML'))
            print(title.get_attribute('href'))
            email_content = email_content + title.get_attribute('innerHTML') + '\n' + title.get_attribute('href') + '\n\n'


        if ban_flag == True:
            print('baned');

        return email_content
