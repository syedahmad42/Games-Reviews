# Import every module/library that we need, here we are using BeautifulSoup
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import time

url='https://www.commonsensemedia.org/reviews/category/game'
#Using time to count how long to process the data
start = time.time()

def getdata(url):
    # Acces the page using request
    page=requests.get(url)
    # Access information related games information
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find_all('div', {'class':'review-info col'})
    # Acces star that exist in the film 
    star = soup.find_all('span', {'class':'rating__score'})
    number = 0
    name = []
    ages = []
    platforms = []
    descriptions = []
    stars = []
    
    for i in star:
        # Extract how many star in every game 
        star = i.find_all('i', {'class':'icon-star-rating active'})
        stars.append(len(star))
        
    stars = pd.DataFrame(stars).astype('int64')
    
    
    for i in table:
        # Extract title in every game 
        title = i.find('a', {'class':'link link--title'}).get_text()
        # Extract the starting age to play in every game 
        age = i.find('span',{'class':'rating__age'}).get_text()
        # Extract all platform that be used in every game
        platform = i.find('div',{'class':'review-product-summary'}).get_text()
        # Extract the descriptions in every game
        description = i.find('p',{'class':'review-one-liner'}).get_text()
        name.append(title)
        ages.append(age)
        platforms.append(platform)
        descriptions.append(description)
        df = pd.DataFrame([name,ages,platforms,descriptions]).T
        #Using RE, we clean some information in the website 
        df[2].replace('[\n]*|(Platforms:)','',regex=True, inplace = True)
        additional = df[2].str.split('(',expand=True)
        additionals = additional[1].str.strip(')\n').astype('int64')
        df[2] = df[2].str.strip()
        df[2].replace("\(\d*\)",'',regex=True, inplace = True)
        df[1] = df[1].replace('[\n]*|(age )|\+','',regex=True).astype('int64')
    # As we loop two times, we need to merge the dataframe 
    data = pd.merge(df,additionals,left_index=True, right_index=True).merge(stars,left_index=True, right_index=True)
    data.rename(columns={'0_x':'name','1_x':'age',2:'platforms',
                        3:'descriptions','1_y':'year','0_y':'star'},inplace=True)
    return data
    

# Test the submit page. if the true, it will take 100 information in 100 pages, if not we need to put how many number we want
submit_page = False 
if submit_page == True:
    number = 100
else: 
    number = int(input())

df = pd.DataFrame()
for i in range(number):
    # Do looping to acces the different pages in website
    new_url = f'https://www.commonsensemedia.org/reviews/category/game/page/{i}'
    data = getdata(new_url)
    df = pd.concat([df,data],ignore_index =True)

display(df)
# Save the data into CSV format 
df.to_csv("games_rate_bs3.csv",header=True, index=False, encoding='utf-8')

end = time.time()
print(end - start)
