# Games-Reviews

How to run Scrapy:
1. Dowload the project and unzip.
2. Open Windows command prompt in Windows OS. 
3. Navigate to the spiders folder within the scrapy project using 'cd' command. For example 'cd C:\Users\PC\Desktop\Games-Reviews-main\Games-Reviews-main\scrapy\Game_reviews\Game_reviews\spiders'
4. Now run command 'scrapy crawl Games'
5. Scrapy will retrieve the data and create a CSV file in spiders folder.

How to run BeautifulSoup
1. Dowload the project and unzip.
2. Using pip install BeautifulSoup, it is better to use addtional library, such as regular expression
3. run in visual studio code or another UI such as spyder
4. Scrapy will display the data and create a CSV file in the folder when you put the code.

How to run Selenium
1. Download the project and unzip
2. Download Selenium, Chrome webdriver and other neccessary packages. If you are using windows, you can read how to download and set up selenium, try tutorial here : https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2
3. Change the web driver path to where it locates on your computer.
4. Run the code using command
5. Chrome web driver will work automatically. Don't do anything with the driver, it will take approximately 7-8 minutes to scrap 100 pages. If you want to test on few pages set boolean operator in the begining of the code to False. 
6. This code will save the output in CSV where you put your code.
