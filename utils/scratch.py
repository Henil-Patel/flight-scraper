from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep


driver = webdriver.Chrome(executable_path="/home/henil/Documents/flight_scraper/flight-scraper/chrome_driver/chromedriver")
url = r"https://www.kayak.com/flights/RDU,IAD-BDQ/2022-11-04/2022-11-18?sort=price_a&attempt=1&lastms=1665022596339"
driver.get(url)
sleep(10)

soup = BeautifulSoup(driver.page_source, 'lxml')
box = soup.find_all("div", class_=r"unrolledTabGrid _iai _itL")
print(box)
driver.quit()

