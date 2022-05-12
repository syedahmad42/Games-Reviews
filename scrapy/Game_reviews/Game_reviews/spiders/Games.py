import scrapy
import pandas as pd
import time

page_limit = True

if page_limit == True: 
    pages = 100
else: pages = 1

#Setting up CSV file
with open('Games.csv','w') as s: 
    s.write("Name, Rating, Review, Year, Platform, Description\n")

start = time.time()

# Defining URL's
class GamesSpider(scrapy.Spider):
    name = 'Games'
    allowed_domains = ['commonsensemedia.org']
    start_urls = ['https://www.commonsensemedia.org/reviews/category/game']
    for i in range(pages):
        start_urls.append('https://www.commonsensemedia.org/reviews/category/game' + "/page/" + str(i))        
  
    # Defining Xpaths       
    def parse(self, response):
        
        name_xpath        = '//h3[@class = "review-title"]/a[@class = "link link--title"]/text()'
        rating_age_xpath       = '//span[@class="rating__age"]/text()'
        rating_score_xpath       = response.xpath('//span[@class="rating__score"]')
        platform_xpath = response.xpath("//div[@class='review-product-summary']/span[1]")
        year_xpath = '//div[@class="review-product-summary"]/span[2]/text()'
        des_xpath = '//p[@class="review-one-liner"]/text()'
        
        #Extract Game Name
        game_name        = response.xpath(name_xpath).getall()
        
        #Extract Game ratings
        rating_age_list       =  response.xpath(rating_age_xpath).getall() 
        rating_age = []
        for x in rating_age_list:
            rating_age.append(x.strip()) 
        
        #Extract Game Reviews
        rating_score = []    
        for rating in rating_score_xpath:
            rating_path = rating.extract()
            rating_stars = rating_path.count('icon-star-rating active')
            rating_score.append(rating_stars)
        
        #Extract Game Year    
        game_year = response.xpath(year_xpath).getall()

        #Extract Game Platform 
        game_platform = []    
        for p in platform_xpath:
            platform = p.xpath('.//a/text()').getall()
            game_platform.append(platform)
        
        #Extract Game Description
        game_des = response.xpath(des_xpath).getall()
        
        # Setup dictionary and export to CSV
        dictionary = {'name': game_name, 'rating': rating_age, 'review': rating_score, 'year':game_year, 'platform':game_platform, 'description':game_des } 
        dataframe = pd.DataFrame(dictionary)
        dataframe['year'] = dataframe['year'].str.replace("(","").str.replace(")","")
        dataframe['platform'] = dataframe['platform'].str.join(', ')
        dataframe.to_csv('Games.csv', mode='a', index=False, header=False)
        
    
        end = time.time()
        print('Here:',end - start)