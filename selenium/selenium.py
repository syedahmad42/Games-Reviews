from genericpath import exists
from pickle import TRUE
from tracemalloc import start
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException


start_time=time.time()


path = "/mnt/c/Users/nomin/chromedriver_linux64/chromedriver"
ser = Service(path)
driver = webdriver.Chrome( service=ser) 

### Following page is the starting page to scrap
url = 'https://www.commonsensemedia.org/game-reviews'

# Actual program:
driver.get(url)

#### To save the output, created empty list for every variable to scrap

game_list=[]
age_rating_list=[]
rating_list=[]
description_list=[]
platform_list=[]
year_list=[]

#### Setting how many pages to scrap 

submit_page = True
if submit_page == True:
    pages=100
else:
    pages=5




#### Using Selenium, Scraping first 100 pages to scrap by clicking next page button
#### In every page there is list of 20 games. So we are scraping every game details from each page. 

for i in range(0,pages): # this is loop for what to do in every page

    #### things to scrap from a page
    ## game name
    games = driver.find_elements(by=By.XPATH,value='//h3[@class="review-title"]')
    for game in range(len(games)):
        game_list.append(games[game].text)
    
    ## game age rating
    age_ratings = driver.find_elements(by=By.XPATH,value='//span[@class="rating__age"]')
    for age_rating in range(len(age_ratings)):
        age_rating_list.append(age_ratings[age_rating].text)

    ## game age rating
    ratings = driver.find_elements(by=By.XPATH,value='//span[@class="rating__score"]')
    for rating in range(len(ratings)):
        rating_string=ratings[rating].get_attribute("innerHTML")
        rating_score=rating_string.count('icon-star-rating active')
        rating_list.append(rating_score)    
    
    ## Short description 
    descs = driver.find_elements(by=By.XPATH,value='//p[@class="review-one-liner"]')
    for desc in range(len(descs)):
        description_list.append(descs[desc].text)
    
    ## In which platform it can be played
    platforms = driver.find_elements(by=By.XPATH,value='//div[@class="review-product-summary"]/span[1]')
    for platform in range(len(platforms)):
        a=platforms[platform].text
        b=a.replace('Platforms: ','')
        platform_list.append(b)
    
    ## Year of release
    years = driver.find_elements(by=By.XPATH,value='//div[@class="review-product-summary"]/span[2]')
    for year in range(len(years)):
        c=years[year].text
        d=c.replace('(','')
        e=d.replace(')','')
        year_list.append(e)
    
    #### To go to next page, we need scroll down till next page link is visible. So that we can click on it

    ##scrolling action
    scroll=driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(by=By.XPATH, value="//li[@class='pagination__next']//a"))
    
    ##next page link location
    click=driver.find_element(by=By.XPATH, value="//li[@class='pagination__next']//a")
    #print("click fine")
    #time.sleep(1)
    click.click()
    #time.sleep(1)
    #print("click click fine")
    #WebDriverWait(driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='pagination__next']//a")))
         
    i+=1 
    time.sleep(3)
    print(i)


#### Closing browser
driver.quit()

#### Saving output to csv
dictionary = {'game_name': game_list, 'age_rating': age_rating_list, 'rating': rating_list, 'description': description_list, 'platform': platform_list, 'year': year_list} 
dataframe = pd.DataFrame(dictionary)
dataframe.to_csv('game_rating.csv')

end_time=time.time()
duration=end_time-start_time
print("*****************here", duration)
